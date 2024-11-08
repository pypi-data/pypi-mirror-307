# SpiceJack

SpiceJack is a tool for generating json questions and answers from documents in python.

[![SpiceJack](https://raw.githubusercontent.com/LIZARD-OFFICIAL-77/SpiceJack/refs/heads/development/images/image.png
)](https://pypi.org/project/spicejack/)

## Usage

```python
from spicejack.pdf import PDFprocessor

def filter1(list):
    """
    Example filter
    """
    return [i.replace("badword","b*dword") for i in list]


processor = PDFprocessor(
    "/path/to/Tax_Evasion_Tutorial.pdf",
    use_legitimate = True, # Runs the processor with the openai api (See "legitimate use")
    filters = (filter1,) # Extra custom filters
)

processor.run(
    thread = True # Runs the processor in a child thread. (threading.Thread)
    process = True # Runs the processor in a child thread. (multiprocessing.Process)
    logging = True # Prints the responses from the LLM
)

```

## Legitimate use

Create a file named .env and put this:

```dotenv
OPENAI_API_KEY = "<YOUR-OPENAI-API-KEY>"
```

## Installation

```bash
pip install spicejack
```

## Support me

You can use SpiceJack for completely free, but donations are very appreciated as I am making this on an 10+ year old laptop.

### Bitcoin

bc1q7xaxer2xpxttm3vpzc8s9dutvck8u9ercxxc95

### Ethereum

0xB7351e098c80E2dCDE48BB769ac14c599E32c47E

### Monero

44Y47Sf2huJV4hx7K1JrTeKbgkPsWdRWSbEiAHRWKroaGYAnxkPjdxhUsDeiFeQ3wc6Tw8v3uYTZMbBUfcdUUgqt5HCqbtY

### Litecoin

LQzd9phuN7iPRn8p5rT1zyVssJ8nY5WjM5

## Roadmap

- [x] Python library

- [ ] Mass generation

- [ ] GUI

## Star History

<a href="https://github.com/">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=LIZARD-OFFICIAL-77/SpiceJack&type=Date">
</a>

## License

<table>
  <tr>
     <td>
       <p align="center"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/1200px-GPLv3_Logo.svg.png" width="80%"></img>
    </td>
    <td> 
      <img src="https://img.shields.io/badge/License-GNU_GPL_v3.0-red.svg"/> <br> 
This project is licensed under <a href="https://github.com/LIZARD-OFFICIAL-77/SpiceJack/blob/development/LICENSE">GNU_GPL_v3.0</a>.
    </td>
  </tr>
</table>

---

<p align="right">(<a href="#top">🔼 Back to top</a>)</p>
