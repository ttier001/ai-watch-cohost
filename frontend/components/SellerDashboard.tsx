'use client'

import { useState } from 'react'
import { classifyMessage, generateResponse, type ProductContext, type ClassifyResponse, type GenerateResponse } from '@/lib/api'

export default function SellerDashboard() {
  // Product form state
  const [product, setProduct] = useState<ProductContext>({
    brand: 'Rolex',
    model: 'Submariner',
    reference: '16610',
    price: 12500,
    year: 1995,
    condition: 'Excellent',
    movement: 'Caliber 3135',
    box_papers: true,
  })

  // Question state
  const [question, setQuestion] = useState('')
  const [isClassifying, setIsClassifying] = useState(false)
  const [classificationResult, setClassificationResult] = useState<ClassifyResponse | null>(null)

  // Response generation state
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedResponse, setGeneratedResponse] = useState<GenerateResponse | null>(null)

  // Error state
  const [error, setError] = useState<string | null>(null)

  const handleClassify = async () => {
    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    setIsClassifying(true)
    setError(null)
    setClassificationResult(null)
    setGeneratedResponse(null)

    try {
      const result = await classifyMessage({
        message: question,
        username: 'test-user'
      })
      setClassificationResult(result)
    } catch (err) {
      setError('Failed to classify message. Check your API connection.')
      console.error(err)
    } finally {
      setIsClassifying(false)
    }
  }

  const handleGenerateResponse = async () => {
    if (!classificationResult) return

    setIsGenerating(true)
    setError(null)

    try {
      const result = await generateResponse({
        question: question,
        product_context: product,
        seller_preferences: {
          tone: 'professional',
          max_length: 150,
          include_username: false
        }
      })
      setGeneratedResponse(result)
    } catch (err) {
      setError('Failed to generate response. Check your API connection.')
      console.error(err)
    } finally {
      setIsGenerating(false)
    }
  }

  const getTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'question': return 'bg-green-100 text-green-800'
      case 'comment': return 'bg-gray-100 text-gray-800'
      case 'spam': return 'bg-red-100 text-red-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">Go Live AI Co-Host</h1>
        <p className="text-gray-600 mt-2">Your AI assistant for live sales</p>
      </div>

      {/* Product Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-4">📦 Product Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Brand</label>
            <input
              type="text"
              value={product.brand}
              onChange={(e) => setProduct({ ...product, brand: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
            <input
              type="text"
              value={product.model}
              onChange={(e) => setProduct({ ...product, model: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Reference Number</label>
            <input
              type="text"
              value={product.reference || ''}
              onChange={(e) => setProduct({ ...product, reference: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
            <input
              type="number"
              value={product.price}
              onChange={(e) => setProduct({ ...product, price: Number(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Year</label>
            <input
              type="number"
              value={product.year || ''}
              onChange={(e) => setProduct({ ...product, year: Number(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Condition</label>
            <select
              value={product.condition}
              onChange={(e) => setProduct({ ...product, condition: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option>Excellent</option>
              <option>Very Good</option>
              <option>Good</option>
              <option>Fair</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Movement</label>
            <input
              type="text"
              value={product.movement || ''}
              onChange={(e) => setProduct({ ...product, movement: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center pt-6">
            <input
              type="checkbox"
              checked={product.box_papers}
              onChange={(e) => setProduct({ ...product, box_papers: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-700">Box & Papers</label>
          </div>
        </div>
      </div>

      {/* Question Classifier */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-4">💬 Test Question Classifier</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Test Question</label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Type a buyer question like 'What movement is in this?'"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleClassify}
            disabled={isClassifying}
            className="w-full bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {isClassifying ? 'Classifying...' : 'Classify Question'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Classification Result */}
      {classificationResult && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">📊 AI Classification</h2>
          <div className="space-y-4">
            <div className="flex gap-2 flex-wrap">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(classificationResult.type)}`}>
                Type: {classificationResult.type}
              </span>
              {classificationResult.topic && (
                <span className="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  Topic: {classificationResult.topic}
                </span>
              )}
              {classificationResult.urgency && (
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getUrgencyColor(classificationResult.urgency)}`}>
                  Urgency: {classificationResult.urgency}
                </span>
              )}
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium">Confidence</span>
                <span>{Math.round(classificationResult.confidence * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${classificationResult.confidence * 100}%` }}
                />
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700 mb-1">AI Reasoning:</p>
              <p className="text-gray-600">{classificationResult.reasoning}</p>
            </div>

            {classificationResult.type.toLowerCase() === 'question' && (
              <button
                onClick={handleGenerateResponse}
                disabled={isGenerating}
                className="w-full bg-green-600 text-white py-3 rounded-md font-semibold hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {isGenerating ? 'Generating Response...' : 'Generate AI Response'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Generated Response */}
      {generatedResponse && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">🤖 AI Generated Response</h2>
          <div className="space-y-4">
            {generatedResponse.requires_review && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p className="text-yellow-800 text-sm font-medium">⚠️ Requires human review before sending</p>
              </div>
            )}

            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-900 text-lg">{generatedResponse.response_text}</p>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium">Confidence</span>
                <span>{Math.round(generatedResponse.confidence * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-600 h-2 rounded-full transition-all"
                  style={{ width: `${generatedResponse.confidence * 100}%` }}
                />
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700 mb-1">AI Reasoning:</p>
              <p className="text-gray-600 text-sm">{generatedResponse.reasoning}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

