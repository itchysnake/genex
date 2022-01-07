# GENEX
<p align="center">
    <a href="https://genex.app/" target="_blank">
        <img src="https://genex.app/wp-content/uploads/2021/09/white_gnx_name-1.gif" alt="logo" width="400"/>
    </a>
    <h4 align="center">Decentralised exchange facilitating human equity securities.</h4>
</p>

<div align="center">
    <a href="https://github.com/itchysnake/genex/blob/master/LICENSE" target="blank">
        <img src="https://img.shields.io/github/license/itchysnake/genex" alt="genex licence"/>
    </a>
    <a href="https://github.com/itchysnake/genex/fork" target="blank">
        <img src="https://img.shields.io/github/forks/itchysnake/genex" alt="genex forks"/>
    </a>
    <a href="https://github.com/itchysnake/genex/issues" target="blank">
        <img src="https://img.shields.io/github/issues/itchysnake/genex" alt="genex issues"/>
    </a>
    <a href="https://github.com/itchysnake/genex/pulls" target="blank">
        <img src="https://img.shields.io/github/issues-pr/itchysnake/genex" alt="genex pull-requests"/>
    </a>
    <img src="https://img.shields.io/github/last-commit/itchysnake/genex" alt="genex last-commit"/>
</div>

<p align="center">
    <a href="https://genex.app" target="blank">Visit GENEX</a>
    ·
    <a href="https://github.com/itchysnake/genex/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/itchysnake/genex/issues/new/choose">Request Feature</a>
</p>

# What is GENEX?
<a href="https://www.youtube.com/watch?v=_gQbdIHU1mA" target="_blank">Watch the video!</a>

`GENEX` is a decentralised exchange deployed on Ethereum specialised in human equity securities. We enable people to invest _directly_ into other people, so that they can use those funds in an economically positive way. By securitising the human productive capacity, we hope to make investments into education in the developing world more stable, incentivisied, and sought-after.
>Read more about [Human Equity Securities](https://genex.app/whitepaper)

# Getting Started
We recommend a local Solidity compiler for testing and deployment. GENEX uses `brownie` to for compiling and debugging, combined with `ganache-cli` to test.

Alternatively you could use `web3.py` directly for compiling and testing.
### Installing eth-brownie
1. To get started with `brownie` you may first need to install `pipx`:
```bash
pipx install eth-brownie
```
2. To check if brownie has been installed:
```bash
brownie
```
>Read more about installing [eth-brownie](https://eth-brownie.readthedocs.io/en/stable/install.html)

### Installing ganache-cli
3. To run a local node for testing, we recommend `ganache-cli` which requires `node.js` and `npm`:
```bash
node -v
```
Version must be > 6.11.5 (we are using v8.1.2)
```bash
npm -v
```
Ensure `npm` is installed.
4. To install `ganache-cli`:
```bash
npm install -g ganache-cli
```
> Read more about installing [node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
