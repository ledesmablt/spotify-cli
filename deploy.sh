#!/bin/bash
# check version
export SPOTIFY_CLI_VERSION=$(git describe)
if [[ -z $SPOTIFY_CLI_VERSION ]]
then
	echo "Please provide a version for deployment."
	echo "export SPOTIFY_CLI_VERSION=(version)"
	exit 1
fi


# confirmation
if [[ "$1" == "production" ]]
then
	# prod build
	DEPLOY="python3 -m twine upload dist/*" 
	echo "!!! This will deploy spotify-cli version $SPOTIFY_CLI_VERSION to PRODUCTION."
else
	# test build
	DEPLOY="python3 -m twine upload --repository testpypi dist/*" 
	echo "This will deploy spotify-cli version $SPOTIFY_CLI_VERSION to test-pypi."
fi

echo "Are you sure? (Y/n)"
read CONFIRM
if [[ "$CONFIRM" != "Y" ]]
then
	echo "User cancelled the operation."
	exit 1
fi


# actual deployment
echo "DEPLOYING"
sudo rm -rf dist/ build/ && \
python3 setup.py sdist bdist_wheel && \
eval $DEPLOY
