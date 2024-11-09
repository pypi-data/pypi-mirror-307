# Creating a Pypi Library

Let's learn how to create and publish a library to pypi using Github Actions.

## Publishing Library 

You can use API keys etc but apparently the best way is to use Trusted Publishers like Github.

So, log into your 

- `Pypi Account > Publishing`

- Here you will see Github, as one of the publishers. 

- Add necessary details to link your library to Github repo.

You are all done.

## Tag A Release

```shell
git tag 0.0.0

git push origin --tags
```
