import "./globals.css";

export const metadata = {
  title: "VeggieVision AI - Vegetable & Fruit Classification System",
  description: "Upload a photo of any vegetable or fruit to instantly identify it, see full nutritional data, learn its health benefits, and get fun facts using deep learning ResNet50.",
  keywords: "vegetable classification, fruit classification, food AI, computer vision, resnet50, deep learning, healthy eating",
  authors: [{ name: "VeggieVision AI Team" }]
};

export default function RootLayout({ children }) {
  return (
    <html lang="vi">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}
