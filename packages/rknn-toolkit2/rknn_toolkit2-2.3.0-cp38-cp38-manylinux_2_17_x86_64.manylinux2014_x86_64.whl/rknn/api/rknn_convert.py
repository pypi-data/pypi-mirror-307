#!/usr/bin/env python3
import sys
import argparse
import json
import os
import subprocess
from multiprocessing import Process, Manager

import yaml
from rknn.api import RKNN


def get_rknn_version(target_platform):
    if target_platform in ['rk1808', 'rk3399pro', 'rv1109', 'rv1126']:
        return 1
    else:
        return 2


def parse_model_config(yaml_config_file):
    with open(yaml_config_file, 'r', encoding='utf-8') as f:
        yaml_config = f.read()
        print(yaml_config)
    model_configs = yaml.load(yaml_config, Loader=yaml.FullLoader)
    return model_configs


def fix_dict_bool_value(items_dict):
    for key, value in items_dict.items():
        if isinstance(value, str):
            if value == 'True' or value == 'true':
                items_dict[key] = True
            elif value == 'False' or value == 'false':
                items_dict[key] = False


def get_input_paths(dataset):
    input_paths = []
    f = open(dataset)
    cwd = os.getcwd()
    os.chdir(os.path.abspath(os.path.dirname(dataset)))
    for lines in f:
        files = lines.strip()
        if files:
            path = []
            for file_ in files.split(' '):
                file = file_.strip()
                if file == '':
                    continue
                path.append(os.path.abspath(file))
            input_paths.append(path)
            break
    f.close()
    os.chdir(cwd)
    return input_paths


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'True'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'False'):
        return False
    elif v.lower() in ('debug'):
        return 'debug'
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def convert_model(config_path, target_platform, out_path, model_name=None, eval_perf_memory=False,
                  accuracy_analysis=False, verbose=False, set_input_size_list_str=None, set_configs=None, device_id=None):
    if config_path is None or target_platform is None or out_path is None:
        print('parameter error')
        return -1

    if config_path:
        yaml_config_file = config_path
    else:
        yaml_config_file = os.path.join(config_path, 'model_config.yml')

    if not os.path.exists(yaml_config_file):
        print('model config %s not exist!' % yaml_config_file)
        return -1

    config_dir = os.path.abspath(os.path.dirname(yaml_config_file))

    print("=========================================")
    print("convert_model:")
    print("  config_path=%s" % config_path)
    print("  config_dir=%s" % str(config_dir))
    print("  out_path=%s" % out_path)
    print("  target_platform=%s" % str(target_platform))
    print("=========================================")

    model_configs = parse_model_config(yaml_config_file)

    print("=========================================")

    rknn_version = get_rknn_version(target_platform)

    model = None
    model = model_configs['models']
    model['configs']['target_platform'] = target_platform

    if model is None:
        print("Error: has not valid model config in %s" % yaml_config_file)
        return -1

    if model_name is None:
        if 'name' in model:
            model_name = model['name']
        else:
            print("error！！！ Please provide the model name")

    # start rknn
    # os.environ["RKNN_BANDWIDTH_PROFILE"] = "1"
    if verbose == None:
        verbose = False
    rknn = RKNN(verbose=verbose)
    # rknn config
    if rknn_version == 1:
        print("Currently not supported for rknn-toolkit1.")
    else:
        # rknn-toolkit2
        if 'mean_values' in model['configs'].keys() and 'std_values' in model['configs'].keys():
            mean_vals = model['configs']['mean_values']
            std_vals = model['configs']['std_values']
        else:
            mean_std = model['configs']['channel_mean_value'].split(' ')
            mean_std = list(map(float, mean_std))
            mean_vals = mean_std[0:-1]
            std_vals = [mean_std[-1]] * len(mean_vals)
            if mean_vals == [-1]:
                mean_vals = None
            if std_vals == [-1]:
                std_vals = None
        rgb2bgr = False
        if 'quant_img_RGB2BGR' in model['configs']:
            rgb2bgr = str2bool(model['configs']['quant_img_RGB2BGR'])
        quantized_dtype = 'asymmetric_quantized-8'
        if 'quantized_dtype' in model['configs']:
            quantized_dtype = model['configs']['quantized_dtype']
        if quantized_dtype == 'asymmetric_quantized-u8':
            quantized_dtype = 'asymmetric_quantized-8'
        quantized_algorithm = 'normal'
        if 'quantized_algorithm' in model['configs']:
            quantized_algorithm = model['configs']['quantized_algorithm']
        quantized_method = 'channel'
        if 'quantized_method' in model['configs']:
            quantized_method = model['configs']['quantized_method']
        optimization_level = 3
        if 'optimization_level' in model['configs']:
            optimization_level = model['configs']['optimization_level']
        model_pruning = False
        if 'model_pruning' in model['configs']:
            model_pruning = str2bool(model['configs']['model_pruning'])
        quantize_weight = False
        if 'quantize_weight' in model['configs']:
            quantize_weight = str2bool(model['configs']['quantize_weight'])
        single_core_mode = False
        if 'single_core_mode' in model['configs']:
            single_core_mode = str2bool(model['configs']['single_core_mode'])
        sparse_infer=False
        if 'sparse_infer' in model['configs']:
            sparse_infer = str2bool(model['configs']['sparse_infer'])
        print("mean_values:" + str(mean_vals))
        print("std_values:" + str(std_vals))
        print("quant_img_RGB2BGR: " + str(rgb2bgr))
        print("quantize: " + str(model['quantize']))
        print("quantized_dtype: " + str(quantized_dtype))
        print("quantized_algorithm: " + str(quantized_algorithm))
        print("target_platform: " + str(target_platform))
        print("quantized_method: " + str(quantized_method))
        print("optimization_level: " + str(optimization_level))
        rknn.config(mean_values=mean_vals,
                    std_values=std_vals,
                    quant_img_RGB2BGR=rgb2bgr,
                    quantized_dtype=quantized_dtype,
                    quantized_algorithm=quantized_algorithm,
                    target_platform=target_platform,
                    quantized_method=quantized_method,
                    optimization_level=optimization_level,
                    model_pruning=model_pruning,
                    quantize_weight=quantize_weight,
                    single_core_mode=single_core_mode,
                    sparse_infer=sparse_infer
                    )
    # load model
    input_size_list = None
    inputs = None
    outputs = None
    if 'subgraphs' in model:
        input_size_list_str = None
        if set_input_size_list_str is not None:
            input_size_list_str = set_input_size_list_str
        else:
            if 'input-size-list' in model['subgraphs']:
                input_size_list_str = model['subgraphs']['input-size-list']
            elif 'input_size_list' in model['subgraphs']:
                input_size_list_str = model['subgraphs']['input_size_list']
        if input_size_list_str:
            input_size_list = []
            for input_size_str in input_size_list_str:
                input_size = list(map(int, input_size_str.split(',')))
                if rknn_version == 2:
                    if len(input_size) == 3:
                        input_size.insert(0, 1)
                input_size_list.append(input_size)
        if 'inputs' in model['subgraphs']:
            inputs = model['subgraphs']['inputs']
        if 'outputs' in model['subgraphs']:
            outputs = model['subgraphs']['outputs']
    model_file_path = ''
    if 'pt_file_path' in model.keys():
        model_file_path = os.path.join(config_dir, model['pt_file_path'])
    elif 'model_file_path' in model.keys():
        model_file_path = os.path.join(
            config_dir, model['model_file_path'])
    if model['platform'] == 'tensorflow':
        rknn.load_tensorflow(tf_pb=model_file_path,
                             inputs=model['subgraphs']['inputs'],
                             outputs=model['subgraphs']['outputs'],
                             input_size_list=input_size_list)
    elif model['platform'] == 'tflite':
        rknn.load_tflite(model=model_file_path)
    elif model['platform'] == 'caffe':
        prototxt_file_path = os.path.join(
            config_dir, model['prototxt_file_path'])
        caffemodel_file_path = os.path.join(
            config_dir, model['caffemodel_file_path'])
        rknn.load_caffe(model=prototxt_file_path,
                        blobs=caffemodel_file_path)
    elif model['platform'] == 'darknet':
        darknet_model_path = os.path.join(
            config_dir, model['darknet_cfg_path'])
        darknet_weight_path = os.path.join(
            config_dir, model['darknet_weights_path'])
        rknn.load_darknet(model=darknet_model_path, weight=darknet_weight_path)
    elif model['platform'] == 'onnx':
        if rknn_version == 2:
            rknn.load_onnx(model=model_file_path, inputs=inputs,
                           outputs=outputs, input_size_list=input_size_list)
        else:
            rknn.load_onnx(model=model_file_path)
    elif model['platform'] == 'pytorch':
        rknn.load_pytorch(model_file_path, input_size_list=input_size_list)
    else:
        print("platform %s not support!" % (model['platform']))
    if 'dataset' in model:
        dataset_path = os.path.join(config_dir, model['dataset'])
    else:
        dataset_path = None
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    if model_name[-5:] == '.rknn':
        model_name = model_name[:-5]
    export_rknn_model_path = "%s.rknn" % (os.path.join(out_path, model_name))
    # build
    ret = rknn.build(do_quantization=model['quantize'], dataset=dataset_path)
    if ret != 0:
        print("rknn build fail " + str(ret))
        return -1
    # export rknn
    ret = rknn.export_rknn(export_path=export_rknn_model_path)
    if ret != 0:
        print("rknn build fail " + str(ret))
        return -1
    print("output rknn path: " + export_rknn_model_path)
    # result = subprocess.run(['md5sum', export_rknn_model_path])

    if eval_perf_memory:
        if device_id == True:
            device_id = None
        ret = rknn.init_runtime(
            target_platform, perf_debug=False, eval_mem=False, device_id=device_id)
        if ret != 0:
            print('Init runtime failed.')
            exit(ret)
        rknn.eval_perf()
        ret = rknn.init_runtime(
            target_platform, perf_debug=False, eval_mem=True, device_id=device_id)
        if ret != 0:
            print('Init runtime failed.')
            exit(ret)
        rknn.eval_memory()
    if accuracy_analysis != None :
            if device_id != None :
                if device_id == True:
                    device_id = None
                ret = rknn.accuracy_analysis(inputs=[accuracy_analysis], target=target_platform, device_id=device_id)
            else:
                ret = rknn.accuracy_analysis(inputs=[accuracy_analysis])
            if ret != 0:
                print('accuracy_analysis failed.')
                exit(ret)
    elif accuracy_analysis != None and dataset_path == None:
        print("error: If accuracy_analysis is turned on, the dataset parameters and content in the yml file must be filled in, otherwise accuracy_analysis will not take effect.")

    results = None

    return results


class ArgumentParser:
    def __init__(self, description):
        self.arguments = {}
        self.description = description

    def add_argument(self, short_name, long_name, description, arg_type=str, required=False, default=None):
        self.arguments[short_name] = {
            "long_name": long_name,
            "description": description,
            "type": arg_type,
            "required": required,
            "default": default
        }

    def parse_args(self):
        import sys
        args = {}
        i = 1
        if len(sys.argv) == 1:
            self.print_help()
            sys.exit(0)
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg.startswith('-'):
                if arg in self.arguments:
                    arg_info = self.arguments[arg]
                    if arg_info["type"] == 'str_and_bool':
                        if not(i+1 < len(sys.argv)) or sys.argv[i+1].startswith('-'):
                            arg_info["type"] = bool
                        else:
                            arg_info["type"] = str
                    if arg_info["type"] != bool:
                        i += 1
                    if i < len(sys.argv) and not sys.argv[i].startswith('-'):
                        value = sys.argv[i]
                        if arg_info["type"] is bool:
                            args[arg_info["long_name"]] = True
                        else:
                            args[arg_info["long_name"]
                                 ] = arg_info["type"](value)
                    elif not (arg_info["type"] is bool or arg_info["type"] == 'str_and_bool'):
                        print(f"Error: Missing value for argument '{arg}'")
                        self.print_help()
                        sys.exit(1)
                    else:
                        args[arg_info["long_name"]] = True
                else:
                    print(f"Error: Unknown argument '{arg}'")
                    self.print_help()
                    sys.exit(1)
            elif arg == '-h' or arg == '--help':
                self.print_help()
                sys.exit(0)
            else:
                print(f"Error: Unknown argument '{arg}'")
                self.print_help()
                sys.exit(1)
            i += 1
        for short_name, arg_info in self.arguments.items():
            if arg_info["required"] and arg_info["long_name"] not in args:
                print(f"Error: Missing required argument '{short_name}'")
                self.print_help()
                sys.exit(1)
        return args

    def print_help(self):
        print(self.description)
        print("Usage: python script.py [OPTIONS]")
        print("Options:")
        for short_name, arg_info in self.arguments.items():
            long_name = arg_info["long_name"]
            description = arg_info["description"]
            required = arg_info["required"]
            default = arg_info["default"]
            if default is not None:
                print(f"  {short_name}, {long_name} : {description} (default: {default})")
            else:
                print(f"  {short_name}, {long_name} : {description}{' (required)' if required else ''}")


if __name__ == '__main__':
    parser = ArgumentParser("Convert Models")
    parser.add_argument('-i', '--input', "yml config file path", required=True)
    parser.add_argument('-o', '--output', "output dir", required=True)
    parser.add_argument('-t', '--target_platform',
                        "target_platform, support rk3568/rk3566/rk3562/rk3588", arg_type=str, required=True)
    parser.add_argument('-e', '--eval_perf_memory',
                        "eval model perf and memory, board debugging is required, multi adb device use -d, default=false", arg_type=bool, default=False)
    parser.add_argument('-a', '--accuracy_analysis',
                        "Usage: -a \"xx1.jpg xx2.jpg\". Simulator accuracy_analysis, if want to turn on board accuracy_analysis, please use -d", arg_type=str, default=None)
    parser.add_argument('-v', '--verbose', "whether to print detailed log information on the screen, default=false", arg_type=bool, default=False)
    parser.add_argument('-d', '--device_id', "Single adb device usage: -d. Multi adb device usage：-d device_id",
                        arg_type='str_and_bool', default=None)

    args = parser.parse_args()
    input_path = args.get('--input', None)
    output_dir = args.get('--output', None)
    target_platform = args.get('--target_platform', None)
    eval_perf_memory = args.get('--eval_perf_memory', None)
    accuracy_analysis = args.get('--accuracy_analysis', None)
    verbose = args.get('--verbose', None)
    device_id = args.get('--device_id', None)
    convert_model(config_path=input_path,
                  out_path=output_dir,
                  target_platform=target_platform,
                  eval_perf_memory=eval_perf_memory,
                  verbose=verbose,
                  accuracy_analysis=accuracy_analysis,
                  device_id=device_id
                  )