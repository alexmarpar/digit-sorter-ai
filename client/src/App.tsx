import { useRef, useState } from "react";
import axios from "axios";
import { ReactSketchCanvas } from "react-sketch-canvas";
import type { ReactSketchCanvasRef } from "react-sketch-canvas";

function App() {
  const canvasRef = useRef<ReactSketchCanvasRef>(null);
  const [prediction, setPrediction] = useState<number | null>(null);

  async function predict() {
    const canvas = canvasRef.current;
    if (!canvas) return;

    try {
      const image = await canvas.exportImage("png");

      const response = await axios.post("http://localhost:8000/predict", {
        image,
      });

      setPrediction(response.data.prediction);
    } catch (error) {
      console.error(error);
    }
  }

  async function clear() {
    const canvas = canvasRef.current;
    if (!canvas) return;

    await canvas.clearCanvas();
    setPrediction(null);
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center justify-center px-4">

      {/* Title */}
      <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center">
        Digit Recognition with AI (NumPy)
      </h1>

      {/* Canvas container */}
      <div className="bg-zinc-900 p-4 rounded-xl shadow-lg border border-zinc-800">
        <ReactSketchCanvas
          ref={canvasRef}
          width="300px"
          height="300px"
          strokeWidth={15}
          strokeColor="black"
          style={{
            borderRadius: "10px",
          }}
        />
      </div>

      {/* Buttons */}
      <div className="flex gap-4 mt-6">
        <button
          onClick={predict}
          className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition font-medium cursor-pointer pointer-events-auto"
        >
          Predecir
        </button>

        <button
          onClick={clear}
          className="px-5 py-2 rounded-lg bg-zinc-700 hover:bg-zinc-600 transition font-medium cursor-pointer pointer-events-auto"
        >
          Limpiar
        </button>
      </div>

      {/* Prediction */}
      <div className="mt-6 text-center">
        <p className="text-zinc-400">Predicción:</p>
        <p className="text-4xl font-bold mt-2 text-green-400">
          {prediction ?? "-"}
        </p>
      </div>

      {/* Footer */}
      <footer className="mt-12 text-sm text-zinc-500 border-t border-zinc-800 pt-6 w-full text-center">
        © {new Date().getFullYear()} Alexmarpar. Todos los derechos reservados.
      </footer>
    </div>
  );
}

export default App;