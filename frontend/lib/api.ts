// Replace with your actual Railway URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-railway-url.up.railway.app'

export interface ClassifyRequest {
  message: string
  username?: string
}

export interface ClassifyResponse {
  type: string
  confidence: number
  topic?: string
  urgency?: string
  reasoning: string
}

export interface ProductContext {
  brand: string
  model: string
  reference?: string
  price: number
  year?: number
  condition: string
  movement?: string
  box_papers: boolean
}

export interface GenerateRequest {
  question: string
  product_context: ProductContext
  seller_preferences?: {
    tone: string
    max_length: number
    include_username: boolean
  }
}

export interface GenerateResponse {
  response_text: string
  confidence: number
  requires_review: boolean
  reasoning: string
  alternative_responses?: string[]
}

export async function classifyMessage(data: ClassifyRequest): Promise<ClassifyResponse> {
  const response = await fetch(`${API_URL}/api/classify-message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  
  if (!response.ok) {
    throw new Error('Classification failed')
  }
  
  return response.json()
}

export async function generateResponse(data: GenerateRequest): Promise<GenerateResponse> {
  const response = await fetch(`${API_URL}/api/generate-response`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  
  if (!response.ok) {
    throw new Error('Response generation failed')
  }
  
  return response.json()
}
