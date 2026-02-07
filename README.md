# 🍳 Pantry Oracle - AI-Powered Recipe Discovery

Your intelligent cooking assistant that finds perfect recipes based on what's in your pantry.

## ✨ Features

- **🔍 Smart Recipe Search** - Find recipes based on available ingredients
- **📸 OCR Ingredient Scanning** - Upload photos of ingredients for automatic detection
- **✍️ Manual Input** - Type in your ingredients with autocomplete suggestions
- **📊 Analytics Dashboard** - Track usage metrics and performance
- **🎨 Beautiful UI** - Modern, responsive design with smooth animations
- **🌶️ Dietary Filters** - Support for vegetarian, vegan, and gluten-free options

## 🚀 Quick Start

### Prerequisites

- **Frontend**: Node.js 18+ and npm
- **Backend**: Python 3.11+ and pip
- **Optional**: Tesseract OCR for image scanning

### Local Development

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/pantry-oracle.git
cd pantry-oracle
```

#### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python app.py
```
Backend runs on: http://localhost:5001

#### 3. Setup Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```
Frontend runs on: http://localhost:3000

#### 4. Open the App
Navigate to http://localhost:3000/profile to start using Pantry Oracle!

## 📁 Project Structure

```
pantry-oracle/
├── frontend/              # Next.js frontend application
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── lib/              # Utility functions and configs
│   └── public/           # Static assets
├── backend/              # Flask backend API
│   ├── api/              # API blueprints
│   ├── services/         # Business logic services
│   ├── ml/               # Machine learning engines
│   ├── data/             # Recipe datasets
│   └── utils/            # Utility functions
├── .github/workflows/    # CI/CD pipelines
└── DEPLOYMENT.md         # Deployment guide
```

## 🌐 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions to production.

### Quick Deploy

**Frontend (Vercel)**:
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/pantry-oracle)

**Backend (Railway)**:
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 🔧 Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5001  # Backend API URL
NODE_ENV=development
```

### Backend (.env)
```bash
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
SECRET_KEY=your-secret-key-change-in-production
```

See `.env.example` files in each directory for complete configuration options.

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel

### Backend
- **Framework**: Flask
- **Language**: Python 3.11
- **ML/Data**: pandas, NumPy, scikit-learn
- **OCR**: Tesseract, pytesseract
- **Deployment**: Railway/Render

## 📊 API Endpoints

### Recipes
- `POST /api/recipes/search` - Search recipes by ingredients
- `GET /api/recipes/:id` - Get recipe details

### OCR
- `POST /api/ocr/scan` - Scan image for ingredients
- `POST /api/ocr/batch` - Batch process multiple images

### Metrics
- `GET /api/metrics/summary` - Get usage summary
- `GET /api/metrics/performance` - Get performance metrics
- `GET /api/metrics/satisfaction` - Get user satisfaction data

### Health
- `GET /health` - Health check endpoint

## 🧪 Testing

### Frontend
```bash
cd frontend
npm run lint
npm run build  # Test production build
```

### Backend
```bash
cd backend
python -m pytest tests/  # When tests are available
flake8 .  # Lint Python code
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Recipe data from [Food.com](https://www.food.com/)
- Icons from [Lucide](https://lucide.dev/)
- UI inspiration from modern cooking apps

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ and 🍳 by the Pantry Oracle team
