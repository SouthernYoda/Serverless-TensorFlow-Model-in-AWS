# Titanic Survivor Prediction

## Commands

```
sam build
```

Deploy dev
```
sam deploy --config-env dev
sam build; sam deploy --config-env dev --no-confirm-changeset --resolve-image-repos
```

Deploy prod
```
sam deploy --config-env prod  --no-confirm-changeset --resolve-image-repos
```

Sample json input:
```
{
    "Pclass": 3,
    "Sex": "male",
    "Age": 22,
    "SibSp": 0,
    "Parch": 0,
    "Fair": 7.25,
    "Embarked": "S"
}
```

# Reference
https://testdriven.io/blog/docker-best-practices/#understand-the-difference-between-entrypoint-and-cmd
https://sysdig.com/blog/dockerfile-best-practices/