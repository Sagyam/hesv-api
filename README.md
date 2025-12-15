# HESV API - Handwritten Equation Solver & Visualizer

[![GitHub license](https://img.shields.io/github/license/Sagyam/Major-Project-Backend?style=for-the-badge)](https://github.com/Sagyam/Major-Project-Backend/blob/backend/LICENSE)

A Django REST API that leverages Computer Vision and Machine Learning to detect, extract, and solve handwritten mathematical equations from images.

## Overview

HESV API combines OpenCV for image processing and TensorFlow for character recognition to:
- Extract handwritten mathematical equations from images using OCR
- Solve systems of linear equations (2D and 3D)
- Solve polynomial equations of any degree
- Convert handwritten equations to Desmos-friendly format

The system uses a custom-trained TensorFlow Lite model that recognizes 19 classes of handwritten characters: digits (0-9), operators (+, -, *, /, =), variables (x, y, z), and decimal points.

## Features

### Image-to-Equation Detection
- **Linear Equation OCR**: Extracts equations like `2x+3y=7` from handwritten images
- **Polynomial Equation OCR**: Detects polynomials with superscript notation (x², x³)
- **Advanced Image Processing**:
  - Handles images with alpha channels
  - Adaptive thresholding for varying lighting conditions
  - Contour-based character segmentation
  - Automatic character bounding box detection

### Equation Solving
- **2D Linear Systems**: Solves two equations with two unknowns (x, y)
- **3D Linear Systems**: Solves three equations with three unknowns (x, y, z)
- **Polynomial Equations**: Solves polynomials of any degree
- **Smart Error Handling**:
  - Detects over/under-determined systems
  - Provides fallback solutions using pseudo-inverse
  - Returns both real and complex solutions for polynomials

## Tech Stack

**Backend Framework:**
- Django 4.0.2
- Django REST Framework 3.13.1
- Gunicorn 20.1.0

**Machine Learning & Computer Vision:**
- TensorFlow CPU 2.7.0
- Keras 2.7.0
- OpenCV 4.5.4.60
- NumPy 1.21.4

**Deployment:**
- Docker
- GitHub Actions (CI/CD)
- Railway

## Project Structure

```
hesv-api/
├── djangoBackend/          # Django project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI application
│
├── majorProject/           # Main application
│   ├── views.py            # API endpoint handlers
│   ├── helper/             # Core algorithms
│   │   ├── linear_detector.py    # Linear equation OCR
│   │   ├── linear_solver.py      # Linear equation solver
│   │   ├── poly_detector.py      # Polynomial OCR
│   │   └── poly_solver.py        # Polynomial solver
│   └── test/               # Test data and test cases
│
├── models/                 # ML models
│   ├── 19_class.h5         # Keras model (44MB)
│   └── tflite_quant_model.tflite  # TFLite quantized model (4MB)
│
├── notebooks/              # Jupyter notebooks for development
├── .github/workflows/      # CI/CD pipeline
└── requirements.txt        # Production dependencies
```

## Installation

### Prerequisites
- Python 3.9+
- pip

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Sagyam/Major-Project-Backend.git
cd Major-Project-Backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. Build the Docker image:
```bash
docker build -t hesv-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 hesv-api
```

### VS Code DevContainer

Open the project in VS Code and use the "Reopen in Container" option. The DevContainer will automatically set up the development environment.

## API Endpoints

Base URL: `/equations/`

### 1. Extract Linear Equation
```http
POST /equations/get-linear-equation
Content-Type: multipart/form-data

image: <file>
```

**Response:**
```json
{
  "equation": "2x+3y=7",
  "debug_logs": [...]
}
```

### 2. Extract Polynomial Equation
```http
POST /equations/get-polynomial-equation
Content-Type: multipart/form-data

image: <file>
```

**Response:**
```json
{
  "equation": "x^3+2.5x^2+x=1.0",
  "desmos_eqn": "x^3+2.5x^2+x-1.0",
  "debug_logs": [...]
}
```

### 3. Solve 2D Linear System
```http
POST /equations/solve-2d-linear-equation
Content-Type: application/x-www-form-urlencoded

equation1=2x+3y=7
equation2=x-y=1
```

**Response:**
```json
{
  "x": 2.0,
  "y": 1.0,
  "error": false,
  "errorMessage": null,
  "warningMessage": null,
  "debug_logs": [...]
}
```

### 4. Solve 3D Linear System
```http
POST /equations/solve-3d-linear-equation
Content-Type: application/x-www-form-urlencoded

equation1=x+y+z=6
equation2=2x-y+3z=14
equation3=x+2y-z=2
```

**Response:**
```json
{
  "x": 3.0,
  "y": 1.0,
  "z": 2.0,
  "error": false,
  "errorMessage": null,
  "warningMessage": null,
  "debug_logs": [...]
}
```

### 5. Solve Polynomial Equation
```http
POST /equations/solve-polynomial-equation
Content-Type: application/x-www-form-urlencoded

equation=x^2-5x+6=0
```

**Response:**
```json
{
  "solutions": ["3.0", "2.0"],
  "solution_type": "real",
  "debug_logs": [...]
}
```

## Testing

The project includes comprehensive unit tests:

```bash
python manage.py test
```

Test coverage includes:
- Linear equation OCR with sample images
- Polynomial equation OCR with sample images
- 2D linear equation solver (20+ test cases)
- 3D linear equation solver (10+ test cases)
- Polynomial equation solver (15+ test cases)

## Machine Learning Model

The character recognition model is a 19-class classifier that recognizes:
- **Digits**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- **Operators**: +, -, *, /, =
- **Variables**: x, y, z
- **Punctuation**: . (decimal point)

**Model Details:**
- Framework: TensorFlow/Keras
- Input: 100x100 grayscale images
- Format: TensorFlow Lite (quantized for production)
- Size: 4MB (TFLite) / 44MB (Keras)

## Development

### Development Dependencies

Install additional development tools:
```bash
pip install -r dev_requirements.txt
```

This includes:
- Jupyter Notebook
- IPython
- Pylint
- Additional visualization tools

### Notebooks

Explore the Jupyter notebooks in the `notebooks/` directory for:
- Linear equation segmentation experiments
- Polynomial segmentation development
- Model training and evaluation

### CI/CD Pipeline

The project uses GitHub Actions to automatically:
- Build Docker images on push/PR to the `backend` branch
- Push images to DockerHub
- Run automated tests

## API Testing

A Postman collection is available in `postman.json`. Import it to test all endpoints with pre-configured examples.

## Known Limitations

- The model works best with clear, well-spaced handwriting
- Supports only single-line equations
- Limited to specific character set (19 classes)
- Complex nested equations are not supported
- Requires equations to be written horizontally

## Future Improvements

- Support for more mathematical symbols (√, π, trigonometric functions)
- Multi-line equation support
- Enhanced superscript/subscript detection
- Integration with graphing capabilities
- Real-time equation solving via webcam

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TensorFlow team for the ML framework
- OpenCV community for image processing tools
- Django and DRF communities for the web framework

## Contact

Sagyam - [@Sagyam](https://github.com/Sagyam)

Project Link: [https://github.com/Sagyam/Major-Project-Backend](https://github.com/Sagyam/Major-Project-Backend)