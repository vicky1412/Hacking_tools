import requests

def download(url):
    result = requests.get(url)
    print(result)

download("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-WaH9McdH4ed6ZezybQfSMRIYmpux045NpryK9bC9CMxdEdciBQ&s")
