{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMStPDJOtVyJ77yfggoqBsy"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "U-jm0TIqlN4M"
      },
      "outputs": [],
      "source": [
        "# SimpleScraper - This program scrapes a website and displays it in clean text.\n",
        "# This code was created with Google Bard on 2023-06-08 08:29:31 PST.\n",
        "\n",
        "\"\"\"\n",
        "Welcome to SimpleScraper!\n",
        "\"\"\"\n",
        "\n",
        "import requests\n",
        "\n",
        "def render_website(url):\n",
        "    response = requests.get(url)\n",
        "    soup = BeautifulSoup(response.content, \"html.parser\")\n",
        "    text = soup.get_text()\n",
        "    text = text.replace('&lt;', '<').replace('&gt;', '>')\n",
        "    text = text.strip()\n",
        "    lines = text.split('\\n')\n",
        "    for line in lines:\n",
        "        if line:\n",
        "            print(line.rstrip())\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    url = input(\"Enter the URL of the website: \")\n",
        "    render_website(url)"
      ]
    }
  ]
}