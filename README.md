#localized-resource

##localized-resource is a python object that encapsulates a localized text (.ini) file that maps error codes to error strings, and text codes to text strings.

---
The format of a localized resources file is that of an ini file. Its name is in the form:

`customName_language.ini`

Where customName is any name your program wants to use, and language represents the language to use (Note: it **IS** permissible to use underscores in the custom name). You need one file
per language you wish to localize your app in.

Tho localization file has two sections (error_codes and messages) in the format:

```
[error_codes]
101=This is error 101
102=This is error 102

[messages]
hello=Hello world.
do_quit=Do you really want to quit?
```

localized-resources also has the ability to manage variables and color formatting. 

Colors may be inserted into either error codes or message with the format: {{COLOR_NAME}}. 

Variables are formatted as {variable_name}. 

So if you wanted a string that displayed (in all red) "Your name is Bob" and Bob was passed as a variable, then the message string could look
like this:

`msg={{COLOR_RED}}Your name is {name}{{COLOR_NONE}}`

(do not forget to turn off the color with {{COLOR_NONE}} at the end or your next text will still be the same color)

---
##Usage:

The localized-resource object is initialized with a path to the .ini file that contains the localized text strings, and a language. If the localized file for that language cannot be found, then the system will default back to English.

Once the object has been initialized, it is simply a matter of requesting a string from this object. If you want to print an error message whose error code is 1001, you would pass this code to the function:

`print(localized_resource_obj.get_error_msg(1001))`

If you want to print out a localized string, the operation is very similar.

`print(localized_resource_obj.get_msg("quit_str")`

If you embed a variable into the string, you can do it using the standard python methodology using the format: {variable_name}

So for example, using the example resource file formatted like this:

```
[messages]
msg={{COLOR_RED}}Your name is {name}{{COLOR_NONE}}
```

You would access the information like this:

```
localized_obj =  LocalizedResource("/path/to/resource/", "myapp", "english")
msg = localized_resource_obj.get_msg(msg)
msg = msg.format(msg="some text to fill into the replace_me variable")
```