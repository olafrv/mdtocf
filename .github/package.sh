# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

VERSION=$(cat ../VERSION)

# Step 0: Build Local Image
docker image rm mdtocf:latest
docker image rm docker.pkg.github.com/olafrv/mdtocf/mdtocf:$VERSION
docker build -t mdtocf ..
# Step 1: Authenticate
echo $GH_TOKEN | docker login docker.pkg.github.com -u olafrv --password-stdin
# Step 2: Tag
docker tag mdtocf:latest docker.pkg.github.com/olafrv/mdtocf/mdtocf:$VERSION
# Step 4: Inspect
docker run --rm -it --entrypoint /bin/bash docker.pkg.github.com/olafrv/mdtocf/mdtocf:$VERSION
# Step 3: Publish
docker push docker.pkg.github.com/olafrv/mdtocf/mdtocf:$VERSION
