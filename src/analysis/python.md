# Using Python (Efficiently)

Python is slow. I can't deny it. But Python, for better
or for worse, has taken over the scientific programming ecosystem
meaning there are a large set of packages that are open source,
professionally maintained, and perform the common tasks that
scientists want to do.

One aspect of Python that has enabled its widespread adoption
(I think) is the relative ease of writing packages in another
programming language. This means that most of our analysis
code will not be using "pure Python", but instead be using
compiled languages (C++ mostly) hidden behind some convenience
wrappers. This is the strategy of many popular Python packages
`numpy`, `scipy`, and the HEP-specific `hist` and `awkward`.

~~~admonish tip title="Biggest Performance Tip"
My biggest tip for any new Python analyzers is to avoid writing
the `for` loop. As mentioned, Python itself is slow, so only
write `for` if you know you are only looping over a small number
of things (e.g. looping over the five different plots you want
to make). We can avoid `for` by using these packages with compiled
languages under-the-hood. The syntax of writing these "vectorized"
operations is often complicated to grasp, but it is concise, precise,
and performant.
~~~


