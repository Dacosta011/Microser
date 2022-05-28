const express = require("express");
const cors = require("cors")
const { Pool, Client } = require("pg");

const db = new Pool({
  user: "postgres",
  host: "localhost",
  database: "Carros",
  password: "root",
  port: 5432,
});

const app = express();
app.use(cors())
app.use(express.json());
db.connect();

app.get("/api2",cors(), async (req, res) => {
  db.query(
    'SELECT id, marca, modelo FROM public."Carro";',
    function (err, result) {
      console.log(result.rows);
      res.send(result.rows);
    }
  );
});

app.get("/api2/:id",cors(), async (req, res) => {
  db.query(
    'SELECT id, marca, modelo FROM public."Carro" WHERE id = ' +
      req.params.id +
      ";",
    function (err, result) {
      console.log(result.rows);
      res.send(result.rows);
    }
  );
});

app.post("/api2",cors(), async (req, res) => {
  const info = req.body;
  db.query(
    'INSERT INTO public."Carro" (id, marca, modelo) VALUES (' +
      info.id +
      ", '" +
      info.marca +
      "', '" +
      info.modelo +
      "');",
    function (err, result) {
      if (!err) {
        res.send("OK");
      } else {
        res.send(err);
      }
    }
  );
});

app.delete("/api2/:id",cors(), async (req, res) => {
  db.query(
    'DELETE FROM public."Carro" WHERE id = ' + req.params.id + ";",
    function (err, result) {
      if (!err) {
        res.send("OK");
      } else {
        res.send(err);
      }
    }
  );
});

app.put("/api2/:id",cors(), async (req, res) => {
  const info = req.body;
  db.query(
    'UPDATE public."Carro" SET marca = \'' +
      info.marca +
      "', modelo = '" +
      info.modelo +
      "' WHERE id = " +
      req.params.id +
      ";",
    function (err, result) {
      if (!err) {
        res.send("OK");
      } else {
        res.send(err);
      }
    }
  );
});

app.listen(3001, () => {
  console.log("Server running on port 3001");
});
