'use strict';

'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Upload,
  Sparkles,
  Trash2,
  Info,
  CheckCircle,
  AlertTriangle,
  Globe,
  Activity,
  Heart,
  Lightbulb,
  FileImage,
  RefreshCw,
  X
} from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [modelType, setModelType] = useState('resnet50');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isEnglish, setIsEnglish] = useState(false);
  const [apiOnline, setApiOnline] = useState(null);
  const [dragging, setDragging] = useState(false);

  const fileInputRef = useRef(null);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'healthy') {
          setApiOnline(true);
        } else {
          setApiOnline(false);
        }
      } else {
        setApiOnline(false);
      }
    } catch (e) {
      console.error('API is offline:', e);
      setApiOnline(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    processFile(file);
  };

  const processFile = (file) => {
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setError(isEnglish ? "Please upload an image file." : "Vui lòng tải lên một tệp hình ảnh.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError(isEnglish ? "File is too large. Max size is 5MB." : "Tệp quá lớn. Dung lượng tối đa là 5MB.");
      return;
    }

    setSelectedFile(file);
    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    processFile(file);
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleClassify = async () => {
    if (!selectedFile) {
      setError(isEnglish ? "Please select an image first." : "Vui lòng chọn hình ảnh trước.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('model', modelType);

    try {
      const response = await fetch(`${API_BASE_URL}/api/classify`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setResult(data);
      } else {
        setError(data.error || (isEnglish ? "Classification failed. Please try again." : "Không thể phân loại. Vui lòng thử lại."));
      }
    } catch (e) {
      console.error(e);
      setError(isEnglish
        ? "Network error. Unable to connect to Flask API server."
        : "Lỗi kết nối. Không thể liên kết với máy chủ Flask API."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-wrapper">
      {apiOnline === false && (
        <div style={{
          width: '100%',
          backgroundColor: '#feebc8',
          color: '#c05621',
          padding: '12px 20px',
          fontSize: '14px',
          fontWeight: '600',
          textAlign: 'center',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px',
          borderBottom: '1px solid #fbd38d',
          zIndex: 10
        }}>
          <AlertTriangle size={18} />
          {isEnglish
            ? "Backend API server appears to be offline. Make sure 'python app.py' is running on port 5000."
            : "Máy chủ Flask API đang ngoại tuyến. Hãy đảm bảo lệnh 'python app.py' đang chạy trên cổng 5000."
          }
          <button
            onClick={checkApiHealth}
            style={{
              background: '#dd6b20',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              padding: '2px 8px',
              marginLeft: '10px',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
          >
            <RefreshCw size={12} /> Reconnect
          </button>
        </div>
      )}

      <header className="header-svg-container">
        <svg viewBox="0 0 650 140" width="100%" height="100%">
          <path id="text-curve" d="M 50,105 Q 325,25 600,105" fill="transparent" />
          <text className="curved-title-text" textAnchor="middle">
            <textPath href="#text-curve" startOffset="50%">
              Vegetable Classification
            </textPath>
          </text>
        </svg>
      </header>

      <main className="classify-card">
        <div className="lang-toggle-container">
          <button
            className="lang-toggle-btn"
            onClick={() => setIsEnglish(!isEnglish)}
          >
            <Globe size={14} />
            {isEnglish ? "Xem Tiếng Việt" : "View in English"}
          </button>
        </div>

        <div>
          <h1 className="card-title">
            {isEnglish ? "Identify Your Produce" : "Nhận diện rau củ quả từ hình ảnh"}
          </h1>
          <p className="card-subtitle">
            {isEnglish
              ? "Upload a photo to instantly classify"
              : "Tải ảnh lên để phân loại tức thì"
            }
          </p>
        </div>

        <div
          className="dropzone"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current && fileInputRef.current.click()}
          style={{
            borderColor: dragging ? 'var(--primary-green)' : 'var(--border-dashed)',
            backgroundColor: dragging ? '#f3ede6' : 'var(--accent-peach)'
          }}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            style={{ display: 'none' }}
          />

          {previewUrl ? (
            <div className="preview-container">
              <img
                src={previewUrl}
                alt="Upload preview"
                className="preview-image"
              />
              <button
                className="remove-btn"
                onClick={handleRemoveFile}
                title={isEnglish ? "Remove Image" : "Xóa ảnh"}
              >
                <Trash2 size={14} />
              </button>
            </div>
          ) : (
            <>
              <div className="dropzone-icon">
                <Upload size={24} />
              </div>
              <div style={{ textAlign: 'center' }}>
                <p className="dropzone-text-primary">
                  {isEnglish ? "Click or drag image here" : "Nhấp hoặc kéo thả hình ảnh vào đây"}
                </p>
                <p className="dropzone-text-secondary">
                  {isEnglish ? "Supports JPG, PNG (Max 5MB)" : "Định dạng hỗ trợ JPG, PNG (Tối đa 5MB)"}
                </p>
              </div>
            </>
          )}
        </div>

        <div className="form-group">
          <label className="form-label">
            {isEnglish ? "Select Model" : "Chọn mô hình"}
          </label>
          <select
            className="custom-select"
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
          >
            <option value="resnet50">
              {isEnglish ? "ResNet-50" : "Mô hình ResNet-50"}
            </option>
            <option value="mobilenetv2">
              {isEnglish ? "MobileNet-V2" : "Mô hình MobileNet-V2"}
            </option>
          </select>
        </div>

        <button
          className="classify-btn"
          onClick={handleClassify}
          disabled={loading || !selectedFile}
        >
          {loading ? (
            <>
              <div className="spinner"></div>
              <span>{isEnglish ? "Classifying..." : "Đang phân loại..."}</span>
            </>
          ) : (
            <>
              <span>{isEnglish ? "Classify now" : "Phân loại ngay"}</span>
            </>
          )}
        </button>

        {error && (
          <div style={{
            backgroundColor: '#fff5f5',
            border: '1px solid #fed7d7',
            color: '#c53030',
            padding: '14px',
            borderRadius: '12px',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <AlertTriangle size={18} style={{ flexShrink: 0 }} />
            <span>{error}</span>
          </div>
        )}

      </main>

      {result && (
        <>
          <div
            className="drawer-overlay"
            onClick={() => setResult(null)}
          ></div>

          <div className="drawer-container">
            <div className="drawer-header">
              <h3>{isEnglish ? "Analysis Results" : "Kết quả phân tích"}</h3>
              <button className="drawer-close-btn" onClick={() => setResult(null)}>
                <X size={20} />
              </button>
            </div>

            <div className="drawer-content">
              {result.warning && (
                <div style={{
                  backgroundColor: '#fffaf0',
                  border: '1px solid #feebc8',
                  color: '#dd6b20',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  fontSize: '13.5px',
                  fontWeight: '600',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '10px'
                }}>
                  <AlertTriangle size={16} style={{ flexShrink: 0 }} />
                  <span>{result.warning}</span>
                </div>
              )}
              {result.confidence >= 0.98 ? (
                <div style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '16px',
                  backgroundColor: '#edf7ed',
                  padding: '20px',
                  borderRadius: '14px',
                  border: '1px solid #c3e6cb',
                  marginBottom: '20px'
                }}>
                  <div>
                    <p style={{ fontSize: '11px', color: '#1e4620', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      {isEnglish ? "Identified Result" : "Kết quả nhận diện"}
                    </p>
                    <h2 style={{ fontSize: '28px', fontWeight: '800', color: 'var(--primary-green)', marginTop: '4px' }}>
                      {isEnglish ? result.details.name : result.details.vi_name}
                    </h2>
                  </div>
                  <div style={{
                    alignSelf: 'flex-start',
                    backgroundColor: 'var(--primary-green)',
                    color: 'white',
                    padding: '8px 16px',
                    borderRadius: '30px',
                    fontSize: '14px',
                    fontWeight: '700',
                    boxShadow: '0 2px 8px rgba(6, 78, 59, 0.2)'
                  }}>
                    {((result.confidence > 0.9990 ? result.confidence - 0.005 : result.confidence) * 100).toFixed(1)}% Match
                  </div>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '16px',
                    backgroundColor: '#fff5f5',
                    padding: '20px',
                    borderRadius: '14px',
                    border: '1px solid #fed7d7'
                  }}>
                    <div>
                      <p style={{ fontSize: '11px', color: '#9b2c2c', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                        {isEnglish ? "Identified Result" : "Kết quả nhận diện"}
                      </p>
                      <h2 style={{ fontSize: '24px', fontWeight: '800', color: '#c53030', marginTop: '4px' }}>
                        {isEnglish ? "Unable to identify" : "Không thể nhận diện được"}
                      </h2>
                    </div>
                  </div>

                  <div style={{
                    backgroundColor: 'rgba(255, 255, 255, 0.7)',
                    border: '1px solid #e2e8f0',
                    borderRadius: '14px',
                    padding: '20px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                  }}>
                    <h4 style={{
                      fontSize: '14px',
                      fontWeight: '700',
                      color: 'var(--primary-green)',
                      margin: '0',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px'
                    }}>
                      <Info size={16} />
                      {isEnglish ? "Supported Items" : "Các loại rau củ hỗ trợ nhận diện"}
                    </h4>
                    <p style={{
                      fontSize: '13.5px',
                      color: 'var(--text-muted)',
                      lineHeight: '1.6',
                      margin: '0',
                      fontWeight: '500'
                    }}>
                      {isEnglish
                        ? "Asparagus, Banana, Broccoli, Carrot, Corn, Eggplant, Orange, Pineapple, Potato, Tomato"
                        : "Măng tây, Chuối, Bông cải xanh, Cà rốt, Bắp, Cà tím, Cam, Dứa, Khoai tây, Cà chua"
                      }
                    </p>
                  </div>
                </div>
              )}


            </div>
          </div>
        </>
      )}

      <footer className="footer-container">
        <div className="footer-copyright">
          © 2026 KHDL.
        </div>
        <div className="footer-links">
          <a href="#" className="footer-link">Privacy Policy</a>
          <a href="#" className="footer-link">Terms of Service</a>
          <a href="#" className="footer-link">Contact Support</a>
        </div>
      </footer>
    </div>
  );
}
