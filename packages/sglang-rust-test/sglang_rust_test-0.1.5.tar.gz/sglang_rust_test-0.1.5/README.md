
- Build rust

```
$ cargo build
```


- Build python binding

We want to add wrapper on top of python binding, so we use Setuptools-rust

Maturin v.s. Setuptools-rust

https://www.perplexity.ai/search/maturin-v-s-setuptools-for-rus-XhFJGCPJSOaThpo2X2QtNA#0


1. editable install

```
$ pip install -e .
```

2. build

```
$ pip install  --index-url="https://pypi.org/simple/" setuptools-rust wheel build
$ python -m build
```
