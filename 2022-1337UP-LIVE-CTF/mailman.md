# Mailman

```
score: 433
solved: 8/12
difficulty: NA
tags: cloud, kubernetes
```

## Problem

```
Who uses the post anymore? Mailing is where it's at!
link https://mailman.ctf.intigriti.io/
Flag format: 1337UP{}
Created by Ignacio Dominguez
```

## Got the flag
The name word-played `postman`, a popular HTTP client used in web development.
The UI allow to put in an URL, choose GET, POST method, set headers... like
Postman.

First trying to access `file://etc/passwd` and got the file content, too easy?
Then try all these files:

- /proc/self/stat to know which user running, pid low number hints this run in a container.
- /proc/self/cmdline to know the command used
- /proc/self/cwd/app.py to read the code
- /proc/self/cwd/app.ini to read the config

None of secret or flag there.

- /proc/self/environ which might contain secret passed as environment, but
  got permission denied.

It seems stuck there.

Go back to `About` page, it advertised:

> About Mailman
>
> Mailman is a online HTTP client for developers to test their APIs. We provide a easy to use UI and the best user experience
> Best performance
>
> At Mailman we garantee 100% uptime thanks to all of our services running in Kubernetes. And the best performance for our customers
> 100% secure!
>
> We take our customer's security very seriously that is why we only use kubernetes secrets to store our most valued secrets.

**use kubernetes (k8s) secrets to store our most valued secrets** is the hint. We
need to find [kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
`secret` is an kubernetes object, which is intended to store secrets like key,
password, but by default, it only stores secrets as base64.

> The name of a Secret object must be a valid DNS subdomain name. You can specify the data and/or the stringData field when creating a configuration file for a Secret. The data and the stringData fields are optional. The values for all keys in the data field have to be base64-encoded strings. If the conversion to base64 string is not desirable, you can choose to specify the stringData field instead, which accepts arbitrary strings as values.

Now we find a way to access kubernetes secret from inside the container (often as ~ a pod in k8s terminology).

Like docker, or AWS EC2 instances, there are always some ways to access info
from "outside", search `Accessing the Kubernetes API from a Pod`
got https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/

So each pod has these files contains info needed

- /var/run/secrets/kubernetes.io/serviceaccount/token - used as Authentiation: bearer header
- /var/run/secrets/kubernetes.io/serviceaccount/ca.crt - we not need here
- /var/run/secrets/kubernetes.io/serviceaccount/namespace - to know which namespace is our container, this case is the `default` namespace.

The API can accessed via `https://kubernetes.default.svc/api`.

Go to each API path to discover until see `secretstuff`:

`https://kubernetes.default.svc/api/v1/namespaces/secretstuff/secrets`

There the base64 encoded flag:

```py
base64.b64decode('MTMzN1VQezAyODMzOTQyODNiODFmZjMwNzgwYzlmMWVmNTYyODQ1fQo=')

b'1337UP{0283394283b81ff30780c9f1ef562845}\n'
```
