# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

# Step 0: Build Local Image
docker build -t md2cf .
# Step 1: Authenticate
echo $GH_TOKEN | docker login docker.pkg.github.com -u olafrv --password-stdin
# Step 2: Tag
docker tag md2cf:latest docker.pkg.github.com/olafrv/md2cf/md2cf:1.0.0-rc1
# Step 3: Publish
docker push docker.pkg.github.com/olafrv/md2cf/md2cf:1.0.0-rc1
