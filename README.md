# python-demo
Python Test and Learn Project

This project uses Python 3.


## Hugging Face Authentication
* Create a new account on [Hugging Face](https://huggingface.co/)
* Create a new token on [Hugging Face](https://huggingface.co/settings/tokens)
* Option 1:
    * Set the environment variable `HF_TOKEN` to the token value.
* Option 2:
  * Use the token to login to Hugging Face CLI (in the virtual environment):
    ```bash
    pip3 install --upgrade huggingface_hub
    huggingface-cli login
    ```
  * The token will be saved to `~/.cache/huggingface/token` file
* To diable the token sent with unnecessary places, set the environment variable `HF_HUB_DISABLE_IMPLICIT_TOKEN=1`.

