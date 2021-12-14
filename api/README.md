## Run
```bash
python app.py
```

## Commande curl pour insérer les similarités dans la bdd

```bash
curl -i -X POST -H 'Content-Type: application/json' -d '{ "name": "P2" }' http://localhost:5000/protein
```

## Code snipet pour l'utiliser dans le projet react
```js
fetch("http://localhost:5000/protein", {
  body: "{ "name": "P2" }",
  headers: {
    "Content-Type": "application/json"
  },
  method: "POST"
})
```