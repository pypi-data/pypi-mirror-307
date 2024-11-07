export ENV_STATE=$1
export VERSION=$2

echo "ENV_STATE=$ENV_STATE"$'\n'"VERSION=$VERSION" > prismstudio/_common/config.env
echo "$VERSION" > VERSION
product_name=""
if [ "prod" == "$ENV_STATE" ]; then
    product_name="\"prismstudio\""
elif [ "stg" == "$ENV_STATE" ]; then
    product_name="\"prismstudio-stg\""
elif [ "dev" == "$ENV_STATE" ]; then
    product_name="\"prismstudio-dev\""
fi

# OS에 따라 적합한 sed 명령어 사용
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|^name =.*|name = $product_name|" pyproject.toml # macOS
else
    sed -i "s|^name =.*|name = $product_name|" pyproject.toml     # Linux & Windows
fi

python -m build

#rm dist/*.tar.gz

#token="pypi-AgEIcHlwaS5vcmcCJDhlYmI1NDIxLWVmYzAtNGNjMy1iODBjLTA4MzUwNWIxMWFhZAACKlszLCI0MmU2MTAyNy04MGI2LTRmOTItOGQyNy1lODAyNjZhMzQxYjciXQAABiCnELWrOcyw9PYTMxHpPDRRqoWnVinztekQBTuVDdhr6w"
#twine upload dist/* -u __token__ -p $token


#PS_FILES="/home/prism/miniconda3/envs/venv/conda-bld/linux-64/prismstudio-*"
#rm $PS_FILES
#conda activate venv
#conda build conda-receipe --no-test
#for f in $PS_FILES
#do
#    echo "Processing $f file..."
#    conda convert -f --platform all $f -o dist/
#done

#ARCH=( "win-64" "osx-arm64" "linux-aarch64" )
#for ar in "${ARCH[@]}"
#do
#    FILES="dist/$ar/*"
#    for f in $FILES
#    do
#        echo "Uploading $f ..."
#        anaconda upload $f
#    done
#done