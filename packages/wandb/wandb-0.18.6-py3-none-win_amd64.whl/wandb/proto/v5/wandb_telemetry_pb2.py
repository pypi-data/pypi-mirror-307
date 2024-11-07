# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wandb/proto/wandb_telemetry.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from wandb.proto import wandb_base_pb2 as wandb_dot_proto_dot_wandb__base__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!wandb/proto/wandb_telemetry.proto\x12\x0ewandb_internal\x1a\x1cwandb/proto/wandb_base.proto\"\xdb\x03\n\x0fTelemetryRecord\x12-\n\x0cimports_init\x18\x01 \x01(\x0b\x32\x17.wandb_internal.Imports\x12/\n\x0eimports_finish\x18\x02 \x01(\x0b\x32\x17.wandb_internal.Imports\x12(\n\x07\x66\x65\x61ture\x18\x03 \x01(\x0b\x32\x17.wandb_internal.Feature\x12\x16\n\x0epython_version\x18\x04 \x01(\t\x12\x13\n\x0b\x63li_version\x18\x05 \x01(\t\x12\x1b\n\x13huggingface_version\x18\x06 \x01(\t\x12 \n\x03\x65nv\x18\x08 \x01(\x0b\x32\x13.wandb_internal.Env\x12%\n\x05label\x18\t \x01(\x0b\x32\x16.wandb_internal.Labels\x12.\n\ndeprecated\x18\n \x01(\x0b\x32\x1a.wandb_internal.Deprecated\x12&\n\x06issues\x18\x0b \x01(\x0b\x32\x16.wandb_internal.Issues\x12\x14\n\x0c\x63ore_version\x18\x0c \x01(\t\x12\x10\n\x08platform\x18\r \x01(\t\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x11\n\x0fTelemetryResult\"\xf5\r\n\x07Imports\x12\r\n\x05torch\x18\x01 \x01(\x08\x12\r\n\x05keras\x18\x02 \x01(\x08\x12\x12\n\ntensorflow\x18\x03 \x01(\x08\x12\x0e\n\x06\x66\x61stai\x18\x04 \x01(\x08\x12\x0f\n\x07sklearn\x18\x05 \x01(\x08\x12\x0f\n\x07xgboost\x18\x06 \x01(\x08\x12\x10\n\x08\x63\x61tboost\x18\x07 \x01(\x08\x12\x10\n\x08lightgbm\x18\x08 \x01(\x08\x12\x19\n\x11pytorch_lightning\x18\t \x01(\x08\x12\x0e\n\x06ignite\x18\n \x01(\x08\x12\x14\n\x0ctransformers\x18\x0b \x01(\x08\x12\x0b\n\x03jax\x18\x0c \x01(\x08\x12\x10\n\x08metaflow\x18\r \x01(\x08\x12\x10\n\x08\x61llennlp\x18\x0e \x01(\x08\x12\x11\n\tautogluon\x18\x0f \x01(\x08\x12\x11\n\tautokeras\x18\x10 \x01(\x08\x12\x10\n\x08\x63\x61talyst\x18\x12 \x01(\x08\x12\x10\n\x08\x64\x65\x65pchem\x18\x15 \x01(\x08\x12\x0f\n\x07\x64\x65\x65pctr\x18\x16 \x01(\x08\x12\x0f\n\x07pycaret\x18\x1c \x01(\x08\x12\x14\n\x0cpytorchvideo\x18\x1d \x01(\x08\x12\x0b\n\x03ray\x18\x1e \x01(\x08\x12\x1a\n\x12simpletransformers\x18\x1f \x01(\x08\x12\x0e\n\x06skorch\x18  \x01(\x08\x12\r\n\x05spacy\x18! \x01(\x08\x12\r\n\x05\x66lash\x18\" \x01(\x08\x12\x0e\n\x06optuna\x18# \x01(\x08\x12\x0f\n\x07recbole\x18$ \x01(\x08\x12\x0c\n\x04mmcv\x18% \x01(\x08\x12\r\n\x05mmdet\x18& \x01(\x08\x12\x11\n\ttorchdrug\x18\' \x01(\x08\x12\x11\n\ttorchtext\x18( \x01(\x08\x12\x13\n\x0btorchvision\x18) \x01(\x08\x12\r\n\x05\x65legy\x18* \x01(\x08\x12\x12\n\ndetectron2\x18+ \x01(\x08\x12\r\n\x05\x66lair\x18, \x01(\x08\x12\x0c\n\x04\x66lax\x18- \x01(\x08\x12\x0c\n\x04syft\x18. \x01(\x08\x12\x0b\n\x03TTS\x18/ \x01(\x08\x12\r\n\x05monai\x18\x30 \x01(\x08\x12\x17\n\x0fhuggingface_hub\x18\x31 \x01(\x08\x12\r\n\x05hydra\x18\x32 \x01(\x08\x12\x10\n\x08\x64\x61tasets\x18\x33 \x01(\x08\x12\x0e\n\x06sacred\x18\x34 \x01(\x08\x12\x0e\n\x06joblib\x18\x35 \x01(\x08\x12\x0c\n\x04\x64\x61sk\x18\x36 \x01(\x08\x12\x0f\n\x07\x61syncio\x18\x37 \x01(\x08\x12\x11\n\tpaddleocr\x18\x38 \x01(\x08\x12\r\n\x05ppdet\x18\x39 \x01(\x08\x12\x11\n\tpaddleseg\x18: \x01(\x08\x12\x11\n\tpaddlenlp\x18; \x01(\x08\x12\r\n\x05mmseg\x18< \x01(\x08\x12\r\n\x05mmocr\x18= \x01(\x08\x12\r\n\x05mmcls\x18> \x01(\x08\x12\x0c\n\x04timm\x18? \x01(\x08\x12\x0f\n\x07\x66\x61irseq\x18@ \x01(\x08\x12\x12\n\ndeepchecks\x18\x41 \x01(\x08\x12\x10\n\x08\x63omposer\x18\x42 \x01(\x08\x12\x10\n\x08sparseml\x18\x43 \x01(\x08\x12\x10\n\x08\x61nomalib\x18\x44 \x01(\x08\x12\r\n\x05zenml\x18\x45 \x01(\x08\x12\x12\n\ncolossalai\x18\x46 \x01(\x08\x12\x12\n\naccelerate\x18G \x01(\x08\x12\x0e\n\x06merlin\x18H \x01(\x08\x12\x0f\n\x07nanodet\x18I \x01(\x08\x12#\n\x1bsegmentation_models_pytorch\x18J \x01(\x08\x12\x1d\n\x15sentence_transformers\x18K \x01(\x08\x12\x0b\n\x03\x64gl\x18L \x01(\x08\x12\x17\n\x0ftorch_geometric\x18M \x01(\x08\x12\x0c\n\x04jina\x18N \x01(\x08\x12\x0e\n\x06kornia\x18O \x01(\x08\x12\x16\n\x0e\x61lbumentations\x18P \x01(\x08\x12\x10\n\x08keras_cv\x18Q \x01(\x08\x12\x10\n\x08mmengine\x18R \x01(\x08\x12\x11\n\tdiffusers\x18S \x01(\x08\x12\x0b\n\x03trl\x18T \x01(\x08\x12\x0c\n\x04trlx\x18U \x01(\x08\x12\x11\n\tlangchain\x18V \x01(\x08\x12\x13\n\x0bllama_index\x18W \x01(\x08\x12\x15\n\rstability_sdk\x18X \x01(\x08\x12\x0f\n\x07prefect\x18Y \x01(\x08\x12\x13\n\x0bprefect_ray\x18Z \x01(\x08\x12\x10\n\x08pinecone\x18[ \x01(\x08\x12\x10\n\x08\x63hromadb\x18\\ \x01(\x08\x12\x10\n\x08weaviate\x18] \x01(\x08\x12\x13\n\x0bpromptlayer\x18^ \x01(\x08\x12\x0e\n\x06openai\x18_ \x01(\x08\x12\x0e\n\x06\x63ohere\x18` \x01(\x08\x12\x11\n\tanthropic\x18\x61 \x01(\x08\x12\x0c\n\x04peft\x18\x62 \x01(\x08\x12\x0f\n\x07optimum\x18\x63 \x01(\x08\x12\x10\n\x08\x65valuate\x18\x64 \x01(\x08\x12\x10\n\x08langflow\x18\x65 \x01(\x08\x12\x12\n\nkeras_core\x18\x66 \x01(\x08\x12\x18\n\x10lightning_fabric\x18g \x01(\x08\x12\x1c\n\x14\x63urated_transformers\x18h \x01(\x08\x12\x0e\n\x06orjson\x18i \x01(\x08\x12\x11\n\tlightning\x18j \x01(\x08\"\xb2\x0c\n\x07\x46\x65\x61ture\x12\r\n\x05watch\x18\x01 \x01(\x08\x12\x0e\n\x06\x66inish\x18\x02 \x01(\x08\x12\x0c\n\x04save\x18\x03 \x01(\x08\x12\x0f\n\x07offline\x18\x04 \x01(\x08\x12\x0f\n\x07resumed\x18\x05 \x01(\x08\x12\x0c\n\x04grpc\x18\x06 \x01(\x08\x12\x0e\n\x06metric\x18\x07 \x01(\x08\x12\r\n\x05keras\x18\x08 \x01(\x08\x12\x11\n\tsagemaker\x18\t \x01(\x08\x12\x1c\n\x14\x61rtifact_incremental\x18\n \x01(\x08\x12\x10\n\x08metaflow\x18\x0b \x01(\x08\x12\x0f\n\x07prodigy\x18\x0c \x01(\x08\x12\x15\n\rset_init_name\x18\r \x01(\x08\x12\x13\n\x0bset_init_id\x18\x0e \x01(\x08\x12\x15\n\rset_init_tags\x18\x0f \x01(\x08\x12\x17\n\x0fset_init_config\x18\x10 \x01(\x08\x12\x14\n\x0cset_run_name\x18\x11 \x01(\x08\x12\x14\n\x0cset_run_tags\x18\x12 \x01(\x08\x12\x17\n\x0fset_config_item\x18\x13 \x01(\x08\x12\x0e\n\x06launch\x18\x14 \x01(\x08\x12\x1c\n\x14torch_profiler_trace\x18\x15 \x01(\x08\x12\x0b\n\x03sb3\x18\x16 \x01(\x08\x12\x0f\n\x07service\x18\x17 \x01(\x08\x12\x17\n\x0finit_return_run\x18\x18 \x01(\x08\x12\x1f\n\x17lightgbm_wandb_callback\x18\x19 \x01(\x08\x12\x1c\n\x14lightgbm_log_summary\x18\x1a \x01(\x08\x12\x1f\n\x17\x63\x61tboost_wandb_callback\x18\x1b \x01(\x08\x12\x1c\n\x14\x63\x61tboost_log_summary\x18\x1c \x01(\x08\x12\x17\n\x0ftensorboard_log\x18\x1d \x01(\x08\x12\x16\n\x0e\x65stimator_hook\x18\x1e \x01(\x08\x12\x1e\n\x16xgboost_wandb_callback\x18\x1f \x01(\x08\x12\"\n\x1axgboost_old_wandb_callback\x18  \x01(\x08\x12\x0e\n\x06\x61ttach\x18! \x01(\x08\x12\x19\n\x11tensorboard_patch\x18\" \x01(\x08\x12\x18\n\x10tensorboard_sync\x18# \x01(\x08\x12\x15\n\rkfp_wandb_log\x18$ \x01(\x08\x12\x1b\n\x13maybe_run_overwrite\x18% \x01(\x08\x12\x1c\n\x14keras_metrics_logger\x18& \x01(\x08\x12\x1e\n\x16keras_model_checkpoint\x18\' \x01(\x08\x12!\n\x19keras_wandb_eval_callback\x18( \x01(\x08\x12\x1d\n\x15\x66low_control_overflow\x18) \x01(\x08\x12\x0c\n\x04sync\x18* \x01(\x08\x12\x1d\n\x15\x66low_control_disabled\x18+ \x01(\x08\x12\x1b\n\x13\x66low_control_custom\x18, \x01(\x08\x12\x18\n\x10service_disabled\x18- \x01(\x08\x12\x14\n\x0copen_metrics\x18. \x01(\x08\x12\x1a\n\x12ultralytics_yolov8\x18/ \x01(\x08\x12\x17\n\x0fimporter_mlflow\x18\x30 \x01(\x08\x12\x15\n\rsync_tfevents\x18\x31 \x01(\x08\x12\x15\n\rasync_uploads\x18\x32 \x01(\x08\x12\x16\n\x0eopenai_autolog\x18\x33 \x01(\x08\x12\x18\n\x10langchain_tracer\x18\x34 \x01(\x08\x12\x16\n\x0e\x63ohere_autolog\x18\x35 \x01(\x08\x12\x1b\n\x13hf_pipeline_autolog\x18\x36 \x01(\x08\x12\x0c\n\x04\x63ore\x18\x37 \x01(\x08\x12\r\n\x05lib_c\x18\x38 \x01(\x08\x12\x0f\n\x07lib_cpp\x18\x39 \x01(\x08\x12\x19\n\x11openai_finetuning\x18: \x01(\x08\x12\x19\n\x11\x64iffusers_autolog\x18; \x01(\x08\x12\x1f\n\x17lightning_fabric_logger\x18< \x01(\x08\x12\x14\n\x0cset_step_log\x18= \x01(\x08\x12\x13\n\x0bset_summary\x18> \x01(\x08\x12\x16\n\x0emetric_summary\x18? \x01(\x08\x12\x13\n\x0bmetric_goal\x18@ \x01(\x08\x12\x15\n\rmetric_hidden\x18\x41 \x01(\x08\x12\x18\n\x10metric_step_sync\x18\x42 \x01(\x08\x12\x13\n\x0bshared_mode\x18\x43 \x01(\x08\"\x96\x02\n\x03\x45nv\x12\x0f\n\x07jupyter\x18\x01 \x01(\x08\x12\x0e\n\x06kaggle\x18\x02 \x01(\x08\x12\x0f\n\x07windows\x18\x03 \x01(\x08\x12\x0e\n\x06m1_gpu\x18\x04 \x01(\x08\x12\x13\n\x0bstart_spawn\x18\x05 \x01(\x08\x12\x12\n\nstart_fork\x18\x06 \x01(\x08\x12\x18\n\x10start_forkserver\x18\x07 \x01(\x08\x12\x14\n\x0cstart_thread\x18\x08 \x01(\x08\x12\x10\n\x08maybe_mp\x18\t \x01(\x08\x12\x10\n\x08trainium\x18\n \x01(\x08\x12\x0b\n\x03pex\x18\x0b \x01(\x08\x12\r\n\x05\x63olab\x18\x0c \x01(\x08\x12\x0f\n\x07ipython\x18\r \x01(\x08\x12\x12\n\naws_lambda\x18\x0e \x01(\x08\x12\x0f\n\x07\x61md_gpu\x18\x0f \x01(\x08\"H\n\x06Labels\x12\x13\n\x0b\x63ode_string\x18\x01 \x01(\t\x12\x13\n\x0brepo_string\x18\x02 \x01(\t\x12\x14\n\x0c\x63ode_version\x18\x03 \x01(\t\"\x9a\x04\n\nDeprecated\x12!\n\x19keras_callback__data_type\x18\x01 \x01(\x08\x12\x11\n\trun__mode\x18\x02 \x01(\x08\x12\x19\n\x11run__save_no_args\x18\x03 \x01(\x08\x12\x11\n\trun__join\x18\x04 \x01(\x08\x12\r\n\x05plots\x18\x05 \x01(\x08\x12\x15\n\rrun__log_sync\x18\x06 \x01(\x08\x12!\n\x19init__config_include_keys\x18\x07 \x01(\x08\x12!\n\x19init__config_exclude_keys\x18\x08 \x01(\x08\x12\"\n\x1akeras_callback__save_model\x18\t \x01(\x08\x12\x18\n\x10langchain_tracer\x18\n \x01(\x08\x12\x1a\n\x12\x61rtifact__get_path\x18\x0b \x01(\x08\x12#\n\x1b\x61rtifactmanifestentry__name\x18\x0c \x01(\x08\x12\x1e\n\x16\x61pi__artifact_versions\x18\r \x01(\x08\x12(\n artifact_collection__change_type\x18\x0e \x01(\x08\x12\x1f\n\x17run__define_metric_copy\x18\x0f \x01(\x08\x12\x14\n\x0crun_disabled\x18\x10 \x01(\x08\x12\x16\n\x0ekeras_callback\x18\x11 \x01(\x08\x12$\n\x1crun__define_metric_best_goal\x18\x12 \x01(\x08\"|\n\x06Issues\x12%\n\x1dsettings__validation_warnings\x18\x01 \x01(\x08\x12!\n\x19settings__unexpected_args\x18\x02 \x01(\x08\x12(\n settings__preprocessing_warnings\x18\x03 \x01(\x08\x42\x1bZ\x19\x63ore/pkg/service_go_protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'wandb.proto.wandb_telemetry_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\031core/pkg/service_go_proto'
  _globals['_TELEMETRYRECORD']._serialized_start=84
  _globals['_TELEMETRYRECORD']._serialized_end=559
  _globals['_TELEMETRYRESULT']._serialized_start=561
  _globals['_TELEMETRYRESULT']._serialized_end=578
  _globals['_IMPORTS']._serialized_start=581
  _globals['_IMPORTS']._serialized_end=2362
  _globals['_FEATURE']._serialized_start=2365
  _globals['_FEATURE']._serialized_end=3951
  _globals['_ENV']._serialized_start=3954
  _globals['_ENV']._serialized_end=4232
  _globals['_LABELS']._serialized_start=4234
  _globals['_LABELS']._serialized_end=4306
  _globals['_DEPRECATED']._serialized_start=4309
  _globals['_DEPRECATED']._serialized_end=4847
  _globals['_ISSUES']._serialized_start=4849
  _globals['_ISSUES']._serialized_end=4973
# @@protoc_insertion_point(module_scope)
