---
layout: post
title: "Radio buttons with Bootstrap and Knockout"
date: 2013-05-28 15:16
comments: true
categories: snippet
tags : [html/css, javascript, bootstrap, knockout, radio button]
---

I'm currently building a web app using [Knockout.js](http://knockoutjs.com/) as a frontend framework, with Bootstrap as my CSS framework.  I wanted to create a button group in which only a single button at a time could be selected (a set of _radio buttons_).  I then wanted to detect when those buttons change value, and which value is subsequently selected.

There are a variety of ways to go about this.  You could solve this using jQuery events, Bootstrap-specific events, or within the Knockout framework.  I decided to do it using a Knockout `click` binding so that once the event does fire, I'm right where I need to be to update my ViewModel, and possibly my backend.

<!-- more -->

Here's what the HTML looks like:

{% codeblock lang:html %}
<div id="radio" class="btn-group" data-toggle="buttons-radio">
	<button type="button" class="btn active" data-bind="click: $root.updateReadPreferences" value="all">All</button>
	<button type="button" class="btn" data-bind="click: $root.updateReadPreferences" value="unread">Unread</button>
</div>
{% endcodeblock %}

And then the JS in my ViewModel:

{% codeblock lang:javascript %}
function FeedsViewModel() {
	...

	self.readPreferences = 'all';

	self.updateReadPreferences = function(koElem, event) {
		var value = $(event.currentTarget).attr('value');
		self.readPreferences = value;
		alert('Unread or all? : ' + value);
	};

	...
}
{% endcodeblock %}

A Knockout event takes the Knockout view object that is in scope for the DOM element as its first parameter - in our case it is the FeedsViewModel.  The second parameter, if provided, is the HTML DOM element that gave rise to the event trigger.  We simply have to use jQuery to ask for the "value" attribute for the DOM element, and then update our ViewModel accordingly.  One downside of this approach is that it is fairly verbose - we need a `value` attribute and a `click` event declared for each button in the button group.  Another way to do it might be to add the `click` event to the button group div instead of each button, but then you have to iterate through the children of the button group checking for the button that has the CSS class `active`.  This creates a race condition between the Knockout event being triggered and Bootstrap updating the CSS.  Since button groups will generally only contain a handful of elements, I found it easiest to just declare the `click` events at the button level.
