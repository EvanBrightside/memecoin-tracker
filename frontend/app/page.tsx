"use client";
import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

interface Token {
  id: number;
  name: string;
  symbol: string;
  current_price: number;
  market_cap: number;
  price_history: number[];
}

export default function Home() {
  const [tokens, setTokens] = useState<Token[]>([]);

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/tokens/market_data")
      .then((response) => response.json())
      .then((data) => {
        setTokens(data);
      })
      .catch((error) => console.error("Ошибка при запросе к API:", error));
  }, []);

  // Получаем даты за последние 7 дней
  const getLast7Days = () => {
    return Array.from({ length: 7 }, (_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - (6 - i));
      return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
    });
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-8 text-yellow-400">Memcoins</h1>
        <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
          {tokens.map((token) => (
            <div key={token.id} className="bg-gray-800 p-6 rounded-lg shadow-lg text-center w-80">
              <h2 className="text-2xl font-semibold mb-2">{token.name} ({token.symbol})</h2>
              <p>Цена: {token.current_price ? `$${token.current_price}` : "Данные отсутствуют"}</p>
              <p>
                Рыночная капитализация: {token.market_cap ? `$${token.market_cap.toLocaleString("ru-RU")}` : "Данные отсутствуют"}
              </p>

              {/* График цены за последнюю неделю */}
              {token.price_history && (
                <div className="my-4">
                  <Line
                    data={{
                      labels: getLast7Days(),
                      datasets: [
                        {
                          label: "Цена за неделю",
                          data: token.price_history,
                          borderColor: "yellow",
                          backgroundColor: "rgba(255, 215, 0, 0.2)",
                          tension: 0.4,
                        },
                      ],
                    }}
                    options={{
                      plugins: { legend: { display: false } },
                      scales: {
                        x: { display: true },
                        y: { display: true },
                      },
                      elements: { point: { radius: 2 } },
                    }}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
