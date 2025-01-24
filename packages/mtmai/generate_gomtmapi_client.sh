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

dst_dir=./mtmai/gomtmclients/rest

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
