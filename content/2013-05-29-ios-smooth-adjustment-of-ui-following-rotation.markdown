Title: iOS: Smooth Adjustment of UI Following Rotation
Category: snippet
Tags: ios, objective-c, uiviewcontroller

Today I came across a small issue when trying to adjust a UIView based on rotation of the device.  The UINavigationController has two main delegate methods that pertain to rotation of the device: `willRotateToInterfaceOrientation:duration:` and `didRotateFromInterfaceOrientation:`.  They are pretty self-explanatory.  The former is called when the view is about to rotate, and provides the destination rotation.  The latter is called when the view rotation animation is over.

The problem I have is that I want to wait until the rotation is over so that I can query the UIViewController's view for its size and then update subviews accordingly.  But if we wait until the `didRotateFromInterfaceOrientation:` method is called, the entire rotation animation is over and then all my views update - it's pretty jerky.  But if I perform my view manipulation in the `willRotate...` method, the view controller's view has not been assigned its new view container yet, so I don't know what the new size of the view is.  

<!-- more -->

I originally thought there might be a function that allows me to ask the view controller what its size will be for a particular rotation, but I couldn't find this anywhere in the docs.  As it turns out, there is a third delegate method that does exactly what I want.  According to [this Stack Overflow response](http://stackoverflow.com/a/4432980/1560633), when the `willAnimateRotationToInterfaceOrientation:duration:` method is called, the view controller's view has already been assigned its destination view container and the animation is about to start.  If I perform my view manipulation then, I know what the view size is about to be, and any changes I make occur at the same time as the actual rotation of the view.  It is a small and easy modification, but makes a big difference.