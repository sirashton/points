import React, { useState, useRef, useEffect } from 'react'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [resultImage, setResultImage] = useState(null)
  const [resultFilename, setResultFilename] = useState(null)
  const [algorithm, setAlgorithm] = useState('ronchetti')
  const [algorithms, setAlgorithms] = useState([]) // Available algorithms
  const [customParams, setCustomParams] = useState({}) // Custom algorithm parameters
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  // Load available algorithms on component mount
  useEffect(() => {
    const loadAlgorithms = async () => {
      try {
        const response = await fetch('/api/algorithms')
        const data = await response.json()
        if (data.success) {
          setAlgorithms(data.algorithms)
          // Set first algorithm as default if none selected
          if (data.algorithms.length > 0 && !algorithm) {
            setAlgorithm(data.algorithms[0].key)
          }
        }
      } catch (err) {
        console.error('Failed to load algorithms:', err)
      }
    }
    
    loadAlgorithms()
  }, [])

  // Handle custom parameter changes
  const handleCustomParamChange = (paramName, value) => {
    setCustomParams(prev => ({
      ...prev,
      [paramName]: value
    }))
  }

  // Initialize custom parameters when algorithm changes
  useEffect(() => {
    const selectedAlg = algorithms.find(alg => alg.key === algorithm)
    if (selectedAlg && selectedAlg.parameters) {
      const initialParams = {}
      selectedAlg.parameters.forEach(param => {
        initialParams[param.name] = param.default
      })
      setCustomParams(initialParams)
    } else {
      setCustomParams({})
    }
  }, [algorithm, algorithms])

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setError(null)
      setResultImage(null) // Clear previous result
      
      // Create preview URL
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    } else {
      setError('Please select a valid image file')
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    handleFileSelect(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleFileInputChange = (e) => {
    const file = e.target.files[0]
    handleFileSelect(file)
  }

  const handleGenerate = async () => {
    if (!selectedFile) {
      setError('Please select an image first')
      return
    }

    setIsProcessing(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('image', selectedFile)
      formData.append('algorithm', algorithm)
      
      // Add all parameters (including dot_size and dot_count if they exist)
      Object.entries(customParams).forEach(([key, value]) => {
        formData.append(key, value)
      })

      const response = await fetch('/api/process', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Processing failed')
      }

      const result = await response.json()
      
      if (result.success) {
        setResultImage(result.image_data)
        setResultFilename(result.filename)
      } else {
        throw new Error(result.error || 'Processing failed')
      }

    } catch (err) {
      setError(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleDownload = () => {
    if (!resultImage) return
    
    // Convert base64 to blob and download
    const link = document.createElement('a')
    link.href = resultImage
    link.download = resultFilename || 'pointillism_result.png'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🎨 Pointillism Generator</h1>
        <p>Transform your photos into beautiful pointillism art ✨</p>
        <div style={{background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4)', color: 'white', padding: '0.5rem 1rem', borderRadius: '20px', fontSize: '0.9rem', fontWeight: '600', marginTop: '1rem', display: 'inline-block', animation: 'pulse 2s infinite'}}>
          🚀 DEPLOYMENT TEST - Changes Working!
        </div>
      </div>

      <div className="controls-section">
        <div className="upload-area-container">
          <div
            className={`upload-area ${selectedFile ? 'has-file' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="upload-icon">📸</div>
            <div className="upload-text">
              {selectedFile ? selectedFile.name : 'Drop your image here or click to browse'}
            </div>
            <div className="upload-subtext">
              Supports JPG, PNG, GIF, and other image formats
            </div>
          </div>
          
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileInputChange}
            style={{ display: 'none' }}
          />
        </div>

        <div className="settings-row">
          <div className="control-group">
            <label className="control-label">Algorithm</label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
              className="algorithm-select"
            >
              {algorithms.map((alg) => (
                <option key={alg.key} value={alg.key}>
                  {alg.name}
                </option>
              ))}
            </select>
            <div className="value-display">
              {algorithms.find(alg => alg.key === algorithm)?.description || 'Loading algorithms...'}
            </div>
          </div>

          {/* Dynamic Custom Parameters */}
          {algorithms.find(alg => alg.key === algorithm)?.parameters?.map((param) => (
            <div key={param.name} className="control-group">
              <label className="control-label">
                {param.label}: {param.type === 'slider' ? customParams[param.name] : ''}
              </label>
              
              {param.type === 'slider' && (
                <>
                  <input
                    type="range"
                    min={param.min}
                    max={param.max}
                    step={param.step || 1}
                    value={customParams[param.name] || param.default}
                    onChange={(e) => handleCustomParamChange(param.name, parseFloat(e.target.value))}
                    className="slider"
                  />
                  <div className="value-display">
                    {param.description}
                  </div>
                </>
              )}
              
              {param.type === 'select' && (
                <>
                  <select
                    value={customParams[param.name] || param.default}
                    onChange={(e) => handleCustomParamChange(param.name, e.target.value)}
                    className="algorithm-select"
                  >
                    {param.options.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                  <div className="value-display">
                    {param.description}
                  </div>
                </>
              )}
              
              {param.type === 'checkbox' && (
                <>
                  <div className="checkbox-container">
                    <input
                      type="checkbox"
                      checked={customParams[param.name] !== undefined ? customParams[param.name] : param.default}
                      onChange={(e) => handleCustomParamChange(param.name, e.target.checked)}
                      className="checkbox-input"
                    />
                    <span className="checkbox-label">{param.label}</span>
                  </div>
                  <div className="value-display">
                    {param.description}
                  </div>
                </>
              )}
            </div>
          ))}


          <button
            onClick={handleGenerate}
            disabled={!selectedFile || isProcessing}
            className="generate-btn"
          >
            {isProcessing ? (
              <>
                <div className="spinner"></div>
                Generating...
              </>
            ) : (
              'Generate Pointillism Art'
            )}
          </button>
        </div>

        {error && <div className="error">{error}</div>}
      </div>

      <div className="images-section">
        <div className="image-container">
          <h3>Original Image</h3>
          {previewUrl ? (
            <img src={previewUrl} alt="Original" className="preview-image" />
          ) : (
            <div className="placeholder-image">
              <div className="placeholder-text">Upload an image to see it here</div>
            </div>
          )}
        </div>

        <div className="image-container">
          <h3>Pointillism Result</h3>
          {resultImage ? (
            <>
              <img src={resultImage} alt="Pointillism Result" className="preview-image" />
              <button onClick={handleDownload} className="download-btn">
                📥 Download Result
              </button>
            </>
          ) : (
            <div className="placeholder-image">
              <div className="placeholder-text">Generate pointillism art to see it here</div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
