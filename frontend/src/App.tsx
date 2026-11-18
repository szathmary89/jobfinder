
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [apiStatus, setApiStatus] = useState("Kapcsolódás...");
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error("A backend hibás választ adott.");
        }
        return response.json();
      })
      .then((data) => {
        setApiStatus(data.status);
      })
      .catch(() => {
        setError("Nem sikerült elérni a backendet.");
      });
  }, []);

  return (
    <main>
      <h1>JobFinder</h1>
      <p>Álláskereső alkalmazás</p>

      <section>
        <h2>Backend kapcsolat</h2>

        {error ? (
          <p>{error}</p>
        ) : (
          <p>API állapot: {apiStatus}</p>
        )}
      </section>
    </main>
  );
}

export default App;
