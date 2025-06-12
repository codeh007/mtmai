#!/bin/bash

set -e

python_client_gen(){
    ROOT_DIR=$(pwd)
    PROJECT_DIR=$(realpath ../../../gomtm)
    GEN_DIR=$(pwd)/mtmai
    dst_dir=$(pwd)/mtmai/clients/rest
    tmp_dir=./tmp
    version=7.3.0
    echo "生成 mtm python sdk \nPROJECT_DIR:${PROJECT_DIR}===>\nGEN_DIR:${GEN_DIR}\n dst_dir:${dst_dir}\n"
    command -v openapi-generator-cli || bun install @openapitools/openapi-generator-cli -g
    mkdir -p $dst_dir

    export JAVA_OPTS="${JAVA_OPTS} -Dlog.level=error"
    openapi-generator-cli generate -i ${PROJECT_DIR}/bin/oas/openapi.yaml -g python -o ./tmp \
        --skip-validate-spec \
        --library asyncio \
        --global-property=apiTests=false \
        --global-property=apiDocs=true \
        --global-property=modelTests=false \
        --global-property=modelDocs=true \
        --config ./openapi-generator-config.yaml \
        --package-name mtmai.clients.rest

    echo "阶段1: 复制目标目录 $tmp_dir/mtmai/clients/rest/models/__init__.py => ${dst_dir}"
    mkdir -p $dst_dir/models
    mkdir -p $dst_dir/api
    cp -r $tmp_dir/mtmai/clients/rest/api $dst_dir/
    cp -r $tmp_dir/mtmai/clients/rest/models $dst_dir/

    rm -rf $tmp_dir
    echo "python_client_gen 完成"

    # GRPC_OUT=${GEN_DIR}/contracts
    # mkdir -p $GRPC_OUT
    # echo "生成 python grpc, GRPC_OUT:${GRPC_OUT} "
    # # python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/api-contracts/dispatcher --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} dispatcher.proto
    # python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/proto/mtmai/mtmpb --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} dispatcher.proto
    # python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/proto/mtmai/mtmpb --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} events.proto
    # python -m grpc_tools.protoc --proto_path=${PROJECT_DIR}/proto/mtmai/mtmpb --python_out=${GRPC_OUT} --pyi_out=${GRPC_OUT} --grpc_python_out=${GRPC_OUT} workflows.proto
    # echo "阶段2: 修正grpc相对导入: ${GRPC_OUT}"
    # OSTYPE=${OSTYPE:-"linux"}
    # if [[ "$OSTYPE" == "darwin"* ]]; then
    #     # macOS
    #     find ${GRPC_OUT} -type f -name '*_grpc.py' -print0 | xargs -0 sed -i '' 's/^import \([^ ]*\)_pb2/from . import \1_pb2/'
    # else
    #     # Linux and others
    #     find ${GRPC_OUT} -type f -name '*_grpc.py' -print0 | xargs -0 sed -i 's/^import \([^ ]*\)_pb2/from . import \1_pb2/'
    # fi
    # echo "修正grpc相对导入 完成"
}
python_client_gen