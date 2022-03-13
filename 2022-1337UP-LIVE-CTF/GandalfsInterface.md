# Gandalf's Interface

```
score: 338
solved: 48/51
difficulty: NA
tags: mobile, java, apk, android
```

## Problem

```
One mobile challenge to rule them all!
Download link: Gandalf Baba.apk
Flag format: Flag{}
Created by Mr.hacker and Sharan Panegav
```

## Got the flag
Download the `apk` file and use http://www.javadecompilers.com/ to decompile APK,
got the source code.

First look at an HTML file at

resources/assets/localwebview.html

which seems to provide a Interface for the app, nothing particular interesting there,
maybe only the word "interface".

In sources/ there is file with name "WebAppInterface"

```
$ find ./sources/com/example
./sources/com/example
./sources/com/example/webview
./sources/com/example/webview/databinding
./sources/com/example/webview/databinding/ActivityWebViewActvitiyBinding.java
./sources/com/example/webview/databinding/ActivityMainBinding.java
./sources/com/example/webview/C0626R.java
./sources/com/example/webview/bitcoincrypt.java
./sources/com/example/webview/WebAppInterface.java
./sources/com/example/webview/WebViewActivity.java
./sources/com/example/webview/MainActivity.java
./sources/com/example/webview/BuildConfig.java
```

or a grep command could help reach that file, too

```java
$ grep flag sources/com/example/
sources/com/example/webview/WebAppInterface.java
70:            queue.add(new StringRequest(0, this.context.getString(C0626R.string.groot) + "?" + param + "=givemeflag", new Response.Listener<String>() {
89:            queue2.add(new StringRequest(0, this.context.getString(C0626R.string.groot) + "?flag=givemeflag", new Response.Listener<String>() {
```

The code around looks like:

```java
    @JavascriptInterface
    public String callcrypt(String param) throws InterruptedException {
        if (Arrays.equals(bitcoincrypt.getsomesalt(param), AUTH_TOKEN)) {
            RequestQueue queue = Volley.newRequestQueue(this.context);
            queue.add(new StringRequest(0, this.context.getString(C0626R.string.groot) + "?" + param + "=givemeflag", new Response.Listener<String>() {
                        ...
            }) {
                public Map<String, String> getHeaders() throws AuthFailureError {
                    Map<String, String> params = new HashMap<>();
                    params.put("User-Agent", bitcoincrypt.getsomeheaders());
                    params.put("Accept-Language", "From JavaScript Interface");
                    return params;
                }
            });
        } else {
            RequestQueue queue2 = Volley.newRequestQueue(this.context);
            queue2.add(new StringRequest(0, this.context.getString(C0626R.string.groot) + "?flag=givemeflag", new Response.Listener<String>() {
                        ...
                public Map<String, String> getHeaders() throws AuthFailureError {
                    Map<String, String> params = new HashMap<>();
                    params.put("User-Agent", bitcoincrypt.getsomeheaders());
                    params.put("Accept-Language", "From JavaScript Interface");
                    return params;
                }
            });
        }
        ...
    }
```

It makes an HTTP GET call to address stored at C0626R.string.groot with custom headers, and params `?flag=givemeflag`.
Find groot in repo

```
$ grep -Rin groot .
./resources/res/values/strings.xml:43:    <string name="groot">https://teambounters.com/shapa.php</string>
```
Access the page see a hint to setup params

```
Ohh - Direct Access is not allowed Perhaps Javascript Interface can assist

Uh oh, Gandalf Rakesh body builder is blocking the way!
Maybe you have a typo in the url? Or you meant to go to a different location? Like...some params ?
```

Follow function definition bitcoincrypt.getsomeheaders()

```java
    public static String getsomeheaders() {
        byte[] bArr = "RheO5PB6mfL5N3YBH45e5XuCEaWpvWUsdgdedgdrddf".getBytes(StandardCharsets.UTF_8);
        byte[] bytes = "Thisnewuseragent".getBytes(StandardCharsets.UTF_8);
        byte[] bArr2 = new byte[bytes.length];
        for (int i = 0; i < bytes.length; i++) {
            bArr2[i] = (byte) (bytes[i] & bArr[i % bArr.length]);
        }
        return new String(bArr2);
    }
```

Google for `java hello world`, create a hello world Java program with the code
of this function to get the User-agent header, with the header, try again:

```py
import requests
r = requests.get('https://teambounters.com/shapa.php',
                 params={'flag': 'givemeflag'},
                headers={'Accept-Language': 'From JavaScript Interface',
                        'User-agent': 'PhaC$@B4ad@!F!H@'})
print(r.text)
# Output:  Your are on right track Try Harder for flag
```

This is the `else` part of the function in WebAppInterface, the if part:

```java
        if (Arrays.equals(bitcoincrypt.getsomesalt(param), AUTH_TOKEN)) {
            RequestQueue queue = Volley.newRequestQueue(this.context);
            queue.add(new StringRequest(0, this.context.getString(C0626R.string.groot) + "?" + param + "=givemeflag", new Response.Listener<String>() {
```

we need to find the secret `param` to access the flag.
The `param` must returns True for `Arrays.equals(bitcoincrypt.getsomesalt(param), AUTH_TOKEN)`.
Copy the AUTH_TOKEN and do a bit reverse coding (xor) to get the param used:

The
```java
import java.nio.charset.StandardCharsets;
class HelloWorld {
    private static String salt = "RheO5PB6mfL5N3YBH45e5XuCEaWpvWUFESqTYnZk";

    public static byte[] getsomesalt(String passparam, byte[] crypt) {
        byte[] bytes = passparam.getBytes();
        byte[] crypt2 = new byte[bytes.length];
        for (int i = 0; i < bytes.length; i++) {
            crypt2[i] = (byte) (bytes[i] ^ crypt[i % crypt.length]);
        }
        return crypt2;
    }

    public static byte[] getsomesalt(String passparam) {
        return getsomesalt(passparam, salt.getBytes());
    }
    private static final byte[] AUTH_TOKEN = {38, 0, 0, 60, 93, 49, 50, 95, 25, 22, 45, 71, 47, 94, 60, 54, 45, 70};

    public static void main(String[] args) {
        byte[] bArr = "RheO5PB6mfL5N3YBH45e5XuCEaWpvWUsdgdedgdrddf".getBytes(StandardCharsets.UTF_8);
        byte[] bytes = "Thisnewuseragent".getBytes(StandardCharsets.UTF_8);
        byte[] bArr2 = new byte[bytes.length];
        for (int i = 0; i < bytes.length; i++) {
            bArr2[i] = (byte) (bytes[i] & bArr[i % bArr.length]);
        }
        System.out.printf("%s\n", new String(bArr2));

        byte[] crypt = salt.getBytes();
        byte[] params = new byte[AUTH_TOKEN.length];
        for (int i = 0; i < AUTH_TOKEN.length; i++) {
            params[i] = (byte) (AUTH_TOKEN[i] ^ crypt[i % crypt.length]);
        }

        System.out.printf("%s", new String(params));
    }
}
```

The param value is `theshapitparameter`, try again access the web:

```py
r = requests.get('https://teambounters.com/shapa.php',
                 params={'theshapitparameter': 'givemeflag'},
                headers={'Accept-Language': 'From JavaScript Interface',
                        'User-agent': 'PhaC$@B4ad@!F!H@'})
print(r.text)
```

Here the flag

`Flag{shapitflagXWs4rg0Ld0LrWxThBkwt}`

## Conclusion
Thanks to reading CODEGATE write-up, I learned to use awesome javadecompilers.com to decompile APK file, the rest is just writing some simple Java code which is doable after some `Java hello world` googling.
