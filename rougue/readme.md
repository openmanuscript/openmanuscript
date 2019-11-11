# RogueWriter: A do-it-yourself distraction-free writing device

It's a writer's dream. Or maybe it's just an obsession. 

**RogueWriter** is a portable device that makes it easy to write, without all the distractions 
that a laptop can offer. I've used a lot of these, and you can take a look at my
article on that obsessive journey.

I wanted something that:

- Was reliable, simple, and flexible
- Was portable, with good battery life
- Was reasonably cheap 
- Was cool, like a clacky, satisfying old typewriter 
- Supported a useful workflow

There are a lot of ways to overplan this, and you can waste a lot of time 3D
printing the perfect case, running wiring diagrams, and stuff like that. 
I didn't want to get lost in that. 
I wanted a design that was easy to build (no soldering or finicky construction). 
The perfect thing would be to buy a bunch of stuff to plugs together, and
ends up being cool. I wanted something I wouldn't be embarrassed to be seen 
using in your local coffee shop.

The design of this thing is important. You'll see that this drives some of 
the purchasing decisions.

So our project breaks into two parts: **1** Connecting some components together 
and **2)** fitting them into a case.

## The Guts

Let's lay this thing out and take a look at the guts. It's basically these
components:

- Computer. This design uses the **Raspberry Pi W**, a small, low-power computer
  that has both wifi and bluethooth on board. This particular design uses a **Pi W** with pre-soldered [GPIO pins](https://www.amazon.com/Raspberry-Pi-Zero-WH-Pre-soldered/dp/B07B8MMD3V).
- Display. The display is pretty important. I've seen a lot of designs for
  things like this using small displays, and they typically have cables and plus
  sticking out of them. I wanted something cleaner, so I chose a [display that lays flat, and has a ribbon connection](https://www.amazon.com/gp/product/B0716RVNTS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).
- Keyboard. Buyer's choice here. There are lots of options for bluetooth
  keyboards, and you can make your own choices on portability, feel, size, etc.
  I have two options that work well for me, and that reliably connect to the
  `pi` over bluetooth. Here's my current [favorite keyboard](https://www.amazon.com/gp/product/B019PIXO78/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).
- Battery, Your choice, based on price, battery life, form factor, etc. A lot of
  different batteries will work, and I always have an eye out for a smaller
  battery pack on sale. 

## Parts List

- A really cool cigar case. This is important, as it sets the parameters of the
  final device. Don't obsess too long about it, though, as you can always take
  these parts and put them into a new, cooler case. In fact, you might say that
  that's kind of the point of this whole thing.
- Raspberry Pi W (includes wireless and bluetooth). This is the compuational
  heart of the device. You don't need much.
- A good battery pack. I've used a number of these, based mostly on price and
  form factor. The form factor is going to be determined by the cigar box and
  the rest of the components.
- Raspberry Pi LCD Hat (important for compactness, and aesthetics
- LCD display of your choice, but here's the one I used. I used it because it
  has a ribbon connector to the `pi`, and that's actually a big part of the
  visual simplicity of the device.
- Miscellaneous USB cables that connect the battery to the `pi`. These will
  vary, depending upon your case, but I found the essential bit is the on/off
  switch. Here's what I ended up using:
    - USB micro cable
    - [USB on/off switch](https://www.amazon.com/gp/product/B07CTHKXDW/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
    - [USB right angle adapter](https://www.amazon.com/gp/product/B01C6031MA/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) I needed this because of the arrangement of the case
      and the size of the battery. You may not need them.
- Full size Plugable foldable bluetooth keyboard ($59)
    - This is one of the only keyboards that I've found that maintains
      a connection with the `pi` through power cycles. It's a nice size, and the
      layout is great for touch typing. It holds a good charge, and turns on/off
      as the keyboard is opened/closed. Nice product.
    - I had originally used a Mac wireless keyboard, but it was a bit too
      expensive for the aesthetic of the device, and it was a bit too big when
      I packed things up. At first, this was the only keyboard that paired with
      the pi robustly.
- Other stuff.
    - Double stick tape. This holds things together well enough to keep
      everything in place, but it can be repositioned if you need to change
      things.
    - Small bit of lighting chain, and two screws to keep the lid in place. You
      may not need this, if your cigar box has some nifty hinges that stay open.
- Tools. All I needed was an x-acto knife to cut the double sided tape, and 
  something to cut the cardboard cover.

## Step I: assemble your parts
1. Assemble the guts of the device.
2. Plug them together to make sure it all works.

## Step II: fit it into the case
This is an ongoing process, but since we aren't soldering, 3D printing, or otherwise specifically making the guts fit the box, we can change it as we use it. So, in this step:

1. Find a nice way to fit everything into your case, and lightly double stick
tape the components in place. This will take some trial and error, but since
you're not soldering or gluing, it's pretty easy to fit things in.

It's important that you let go of making this some futzy, crazy, perfect thing.
Some tape and bubble gum keeping it together is a good thing.

## OS/Software

Next, you should [install the OS for your PI](http://someplace.html). Or, easier
still, you can buy a memory card that has the [OS
pre-installed.](http://someplace.html)

Now that you have a **RogueWriter** up and running, you have a choice. What workflow
do you want to support? The native OS for the `pi` is `Raspbian`, and it is
very flexible. You can easily:
    
- Use the computer as a normal Linux-based desktop, and use tools that work in
  that environment. This is great for most people, but it will require you to
  pair a mouse with the computer, as well. If that's what you want to do, that
  should work fine.
- Set up things to work in a terminal-only mode. If this option makes sense to
  you, you're closer to making a more distraction-free **RogueWriter**. 


