# What this is
This is a special vectorization process and helper, using the [vectorization-server](https://github.com/volvo-cars-se/vectorization-server.git) as BE. It takes any arbitrary dictionary object and vectorizes all properties.
`index` property is a string or integer value. The top index value, and input to vectorize function, is the name of the object you send in. If you don't want to specify anything specific then just leave it. It doesn't affect anything. 

# How to install
```bash
pip install -U vecsdk
```

# How to use
```python
from vecsdk import VectorizationServer, VectorGroup

vectorize = VectorizationServer(host="...", port=5678)
vector_group: VectorGroup = vectorize(
    data={
        'a': {
            'c': "hello",
            'd': 1.0,
        }, 
        'b': [
            {
                'e': "world",
                'f': 2.0,
            },
            {
                'g': "!",
                'h': 2.0,
            },
        ],
    },
    index="my_object",
) 
```

`vector_group` is a `VectorGroup` object which has the `aggregate` function. So to get one single vector representing the whole object you'll use `vector_group.aggregate()`.

```python
# Aggregate into a single vector representing the whole object
single_vector = vector_group.aggregate()
```

The aggregate function takes a `weight` dictionary object where you could weight certain properties to increase or decrease. The default aggregate function is the `np.mean`, but you can use whatever fits you.

```python
# Adding some bias/weights to the final single vector representation
# In the end, 'a' aggregated vector property will have less effect on the final vector whereas 'g' will have large effect. Default weight value is 1.0.
biased_single_vector = vector_group.aggregate({'a': 0.2, 'g': 3})
```