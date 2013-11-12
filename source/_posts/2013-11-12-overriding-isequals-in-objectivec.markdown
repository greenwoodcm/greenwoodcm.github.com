---
layout: post
title: "Overriding isEquals in Objective-C"
date: 2013-11-12 07:44
comments: true
categories: snippet
tags: [ios, objective-c, hash, isequals]
---

I am currently working on a small personal project, an iPhone app written in Objective-C.  I needed a simple data structure to hold a 2-element tuple of integers.  I originally implemented this as a C-struct:

{% codeblock lang:objc %}
struct Index {
    NSInteger row;
    NSInteger column;
};
typedef struct Index Index;
{% endcodeblock %}

This worked fine, but I often found myself doing a multiline declare-then-set-members pattern every time I wanted to use the data structure.  To simplify, I added a small C function to generate structs, similar to `CGRectMake`:

<!-- more -->

{% codeblock lang:objc %}
Index IndexMake(NSInteger r, NSInteger c)
{
    Index index;
    index.row = r;
    index.column = c;
    return index;
}
{% endcodeblock %}

This worked great until I needed to put the data structure into a collection such as an NSMutableSet.  Because the contained objects in such a collection need to be Objective-C pointers, you need to encapsulate the struct.  According to [this SO post](http://stackoverflow.com/questions/4516991/whats-the-best-way-to-put-a-c-struct-in-an-nsarray), the correct way to do so is this:

{% codeblock lang:objc %}
Index index = IndexMake(i, j);
[selectedIndices addObject:[NSValue valueWithBytes:&index objCType:@encode(Index)]]
{% endcodeblock %}

So this is now starting to get a bit ugly.  Once I realized that I would be using this data structure all throughout my app, I decided it would be way easier to just make it a proper Objective-C class.

{% codeblock lang:objc %}
@interface GridIndex : NSObject
@property (nonatomic) NSInteger row;
@property (nonatomic) NSInteger column;
@end
{% endcodeblock %}

With a static initializer, this really cleaned up the dependent code.  Of course, this also promptly broke the entire program.  Why?  Because I hadn't overridden the default `isEqual:` method in my custom class.  My first attempt at doing so did not work as expected:

{% codeblock lang:objc %}
-(BOOL)isEqual:(id)object
{
    if(![(NSObject*)object isKindOfClass:[GridIndex class]])
        return NO;
    GridIndex *other = (GridIndex*)object;
    return self.row == other.row && self.column == other.column;
}
{% endcodeblock %}

After adding a bunch of debugging I realized that the problem was when checking if an NSSet contained a GridIndex with a specific row and column.  More debugging showed that my `isEqual:` method was not called deterministically by the set containment method.  Sometimes my overridden function was called and worked as expected, sometimes it was totally bypassed and the result was always false.

After some more research, [this post](http://nshipster.com/equality/) gave me the answer.  As it turns out, to override `isEquals:` in Objective-C you are actually expected to do three things.

> - Implement a new `isEqualTo__ClassName__:` method, which performs the meaningful value comparison.
> - Override `isEqual:` to make class and object identity checks, falling back on the aforementioned value comparison method.
> - Override `hash`.

Doing so fixed the problem.  Good thing someone had already written on this issue because I did not realize all of this was strictly necessary when overriding a simple `isEquals:` method.

Here's my final implementation:

{% codeblock lang:objc %}
-(BOOL)isEqualToGridIndex:(GridIndex*)other
{
    return self.row == other.row && self.column == other.column;
}

-(BOOL)isEqual:(id)object
{
    if(![(NSObject*)object isKindOfClass:[GridIndex class]])
        return NO;
    return [self isEqualToGridIndex:(GridIndex*)object];
}

-(NSUInteger)hash
{
    return self.row + self.column;
}
{% endcodeblock %}