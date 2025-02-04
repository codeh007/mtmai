#!/bin/bash

set -e

ROOT_DIR=$(pwd)
PROJECT_DIR=$(realpath ../../../gomtm)
GEN_DIR=$(realpath ./mtmaisdk)

ROOT_DIR=$(pwd)

echo "生成 mtm python sdk PROJECT_DIR:${PROJECT_DIR}, GEN_DIR:${GEN_DIR}"

# deps
version=7.3.0

command -v openapi-generator-cli || npm install @openapitools/openapi-generator-cli -g

dst_dir=./mtmaisdk/clients/rest

mkdir -p $dst_dir

tmp_dir=./tmp
# generate into tmp folder
openapi-generator-cli generate -i ${PROJECT_DIR}/bin/oas/openapi.yaml -g python -o ./tmp --skip-validate-spec \
    --library asyncio \
    --global-property=apiTests=false \
    --global-property=apiDocs=true \
    --global-property=modelTests=false \
    --global-property=modelDocs=true \
    --package-name mtmaisdk.clients.rest

mv $tmp_dir/mtmaisdk/clients/rest/api_client.py $dst_dir/api_client.py
mv $tmp_dir/mtmaisdk/clients/rest/configuration.py $dst_dir/configuration.py
mv $tmp_dir/mtmaisdk/clients/rest/api_response.py $dst_dir/api_response.py
mv $tmp_dir/mtmaisdk/clients/rest/exceptions.py $dst_dir/exceptions.py
mv $tmp_dir/mtmaisdk/clients/rest/__init__.py $dst_dir/__init__.py
mv $tmp_dir/mtmaisdk/clients/rest/rest.py $dst_dir/rest.py

openapi-generator-cli generate -i ${PROJECT_DIR}/bin/oas/openapi.yaml -g python -o . --skip-validate-spec \
    --library asyncio \
    --global-property=apis,models \
    --global-property=apiTests=false \
    --global-property=apiDocs=false \
    --global-property=modelTests=false \
    --global-property=modelDocs=false \
    --package-name mtmaisdk.clients.rest

# copy the __init__ files from tmp to the destination since they are not generated for some reason
cp $tmp_dir/mtmaisdk/clients/rest/models/__init__.py $dst_dir/models/__init__.py
cp $tmp_dir/mtmaisdk/clients/rest/api/__init__.py $dst_dir/api/__init__.py

# remove tmp folder
rm -rf $tmp_dir

# 暂时 跳过 grpc 相关的代码生成 （因为当前环境报错）
# 使用python 的方式
# uv pip install grpc_tools

python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/dispatcher --python_out=${GEN_DIR}/contracts --pyi_out=${GEN_DIR}/contracts --grpc_python_out=${GEN_DIR}/contracts dispatcher.proto
python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/events --python_out=${GEN_DIR}/contracts --pyi_out=${GEN_DIR}/contracts --grpc_python_out=${GEN_DIR}/contracts events.proto
python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/workflows --python_out=${GEN_DIR}/contracts --pyi_out=${GEN_DIR}/contracts --grpc_python_out=${GEN_DIR}/contracts workflows.proto

OSTYPE=${OSTYPE:-"linux"}
# Fix relative imports in _grpc.py files
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    find ${GEN_DIR}/contracts -type f -name '*_grpc.py' -print0 | xargs -0 sed -i '' 's/^import \([^ ]*\)_pb2/from . import \1_pb2/'
else
    # Linux and others
    find ${GEN_DIR}/contracts -type f -name '*_grpc.py' -print0 | xargs -0 sed -i 's/^import \([^ ]*\)_pb2/from . import \1_pb2/'
fi

# 生成服务器端代码 (openapi-generator-cli 的fastapi 生成功能不够好,改用 : fastapi-code-generator)
#


# echo "生成服务器端代码到: ${server_dst_dir}"

# openapi-generator-cli generate \
#     -i ${PROJECT_DIR}/bin/oas/openapi.yaml \
#     -g python-fastapi \
#     -o $server_dst_dir \
#     --skip-validate-spec \
#     --package-name mtmaisdk.server \
#     --source-folder testabc

echo "=========================================================================="
echo "使用 fastapi-code-generator 生成服务器端代码"
echo "=========================================================================="
# 提示: 1:使用 openapi-generator-cli -g 是能够生成服务器端代码,但是总感觉不是那么回事
#      2: 使用 fastapi-codegen 不能生成服务器端代码,原因是 fastapi-codegen 不能正确处理复杂的 openapi.yaml ,
#         当前一直报错,无法正确生成
#      3: fastapi-codegen 实际底层使用了 datamodel-codegen, 可以使用 datamodel-codegen 生成相关的 models 结构.
#      4: 对于服务器的实现最好不要使用完全的服务器生成,仅生成 components(models)的结构就够了.
# command -v fastapi-codegen || uv pip install fastapi-code-generator

# fastapi-codegen --input ${PROJECT_DIR}/bin/oas/openapi.yaml \
#     --output ./mtmai/server \
#     --output-model-type pydantic.BaseModel


# server_dst_dir=./mtmai/server
# mkdir -p $server_dst_dir
# # 先生成数据模型
# datamodel-codegen --input ${PROJECT_DIR}/bin/oas/openapi.yaml \
#     --output ./mtmai/server/models.py \
#     --target-python-version 3.12 \
#     --use-schema-description \
#     --use-annotated \
#     --use-field-description \
#     --field-constraints


gen_gomtmclient(){
    ROOT_DIR=$(pwd)
    PROJECT_DIR=$(realpath ../../../gomtm)
    dst_dir=./mtmai/gomtmclients/rest
    # GEN_DIR=$(realpath ./mtmaisdk)

    # echo "生成 mtm python sdk PROJECT_DIR:${PROJECT_DIR}, GEN_DIR:${GEN_DIR}"

    # deps
    # version=7.3.0

    command -v openapi-generator-cli || npm install @openapitools/openapi-generator-cli -g
    mkdir -p $dst_dir
    # 因为 openapi-generator-cli 会生成完整python project, 有很不必要的文件
    tmp_dir=/tmp
    # generate into tmp folder
    openapi-generator-cli generate -i ${PROJECT_DIR}/bin/oas/openapi.yaml -g python -o ${tmp_dir} --skip-validate-spec \
        --library asyncio \
        --global-property=apiTests=false \
        --global-property=apiDocs=true \
        --global-property=modelTests=false \
        --global-property=modelDocs=true \
        --package-name mtmai.gomtmclients.rest

    #将库文件复制到目标路径
    cp -r $tmp_dir/mtmai/gomtmclients/ ./mtmai/
}
gen_gomtmclient