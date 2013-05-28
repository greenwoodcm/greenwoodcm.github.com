---
layout: post
title: "RestKit POST with nested data"
description: ""
category: snippet
tags: [ios, restkit, objective-c]
---

I am using [RestKit](http://www.restkit.org) to map objects in my iPhone application to RESTful requests to my [Flask](http://flask.pocoo.org/) server.  I have to use RKRequestMapping to specify the format of the data a POST request expects.  This works fine when the data is flat, but I had trouble when there was an array of nested mappings that needed to be accounted for.  For example, here is the object that will be passed as data to the POST request:

<!-- more -->

{% codeblock lang:objc %}
@interface TestArgs : NSObject

@property (copy, nonatomic) NSString *name;
@property (strong, nonatomic) NSArray *users;

end
{% endcodeblock %}

The users array is an array of dictionaries, each containing the keys {'id', 'type'}.  What I expected to see on the Flask end in the `request.form` variable was:

{% highlight python %}
{'name': 'theName', 'users': [{'id':1, 'type':'user'},{'id':2,'type':'admin'}]}
{% endhighlight %}

What I actually got was:

{% codeblock lang:python %}
{'name': 'theName', 'users[]["id"]': 1, 'users[]["id"]': 2, 'users[]["type"]': 'user', 'users[]["type"]': 'admin'}
{% endcodeblock %}

Not very helpful.  The reason this happens is that form data is generally encoded in URL encoding, not JSON encoding.  URL encoding doesn't handle array values very well, so I needed to use JSON encoding to capture the nested information I wanted to send.  Took me a while, but as it turns out I had to change two things in my code to make this work.  First, on the client side, I had to change the serialization type that RestKit uses to serialize POST data:

{% codeblock lang:objc %}
RKObjectManager *objectManager = ...
[objectManager setRequestSerializationMIMEType:RKMIMETypeJSON];
{% endcodeblock %}

Second, on the server side, I had to access the JSON data that was submitted with the POST differently:

{% codeblock lang:python %}
post_data = request.json
user_array = post_data['users']
{% endcodeblock %}