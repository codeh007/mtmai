#!/bin/bash

set -e

python_client_gen(){
    ROOT_DIR=$(pwd)
    PROJECT_DIR=$(realpath ../../../gomtm)
    GEN_DIR=$(pwd)/mtmai
    dst_dir=$(pwd)/mtmai/clients/rest
    tmp_dir=./tmp
    version=7.3.0
    echo "生成 mtm python sdk PROJECT_DIR:${PROJECT_DIR}, GEN_DIR:${GEN_DIR}\n dst_dir:${dst_dir}"
    command -v openapi-generator-cli || npm install @openapitools/openapi-generator-cli -g
    mkdir -p $dst_dir

    openapi-generator-cli generate -i ${PROJECT_DIR}/bin/oas/openapi.yaml -g python -o ./tmp --skip-validate-spec \
        --library asyncio \
        --global-property=apiTests=false \
        --global-property=apiDocs=true \
        --global-property=modelTests=false \
        --global-property=modelDocs=true \
        --package-name mtmai.clients.rest

    # mv $tmp_dir/mtmaisdk/clients/rest/api_client.py $dst_dir/api_client.py
    # mv $tmp_dir/mtmaisdk/clients/rest/configuration.py $dst_dir/configuration.py
    # mv $tmp_dir/mtmaisdk/clients/rest/api_response.py $dst_dir/api_response.py
    # mv $tmp_dir/mtmaisdk/clients/rest/exceptions.py $dst_dir/exceptions.py
    # mv $tmp_dir/mtmaisdk/clients/rest/__init__.py $dst_dir/__init__.py
    # mv $tmp_dir/mtmaisdk/clients/rest/rest.py $dst_dir/rest.py

    # openapi-generator-cli generate -i ${PROJECT_DIR}/bin/oas/openapi.yaml -g python -o . --skip-validate-spec \
    #     --library asyncio \
    #     --global-property=apis,models \
    #     --global-property=apiTests=false \
    #     --global-property=apiDocs=false \
    #     --global-property=modelTests=false \
    #     --global-property=modelDocs=false \
    #     --package-name mtmaisdk.clients.rest

    echo "阶段1: 复制 api 和 models 到目标目录 $tmp_dir/mtmai/clients/rest/models/__init__.py => ${dst_dir}"
    # copy the __init__ files from tmp to the destination since they are not generated for some reason
    mkdir -p $dst_dir/models
    cp $tmp_dir/mtmai/clients/rest/models/__init__.py $dst_dir/models/__init__.py
    mkdir -p $dst_dir/api
    cp $tmp_dir/mtmai/clients/rest/api/__init__.py $dst_dir/api/__init__.py

    echo "阶段1: 复制 api 和 models 到目标目录 ${dst_dir}"
    mkdir -p $dst_dir/api
    cp -r $tmp_dir/mtmai/clients/rest/api $dst_dir/
    mkdir -p $dst_dir/models
    cp -r $tmp_dir/mtmai/clients/rest/models $dst_dir/

    # remove tmp folder
    rm -rf $tmp_dir

    # uv pip install grpc_tools
    GRPC_OUT=${GEN_DIR}/contracts
    mkdir -p $GRPC_OUT
    echo "生成 python grpc, GRPC_OUT:${GRPC_OUT} "
    python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/dispatcher --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} dispatcher.proto
    python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/events --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} events.proto
    python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/workflows --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} workflows.proto
    echo "阶段2: 修正grpc相对导入: ${GRPC_OUT}"
    OSTYPE=${OSTYPE:-"linux"}
    # Fix relative imports in _grpc.py files
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        find ${GEN_DIR}/contracts -type f -name '*_grpc.py' -print0 | xargs -0 sed -i '' 's/^import \([^ ]*\)_pb2/from . import \1_pb2/'
    else
        # Linux and others
        find ${GEN_DIR}/contracts -type f -name '*_grpc.py' -print0 | xargs -0 sed -i 's/^import \([^ ]*\)_pb2/from . import \1_pb2/'
    fi

}
python_client_gen