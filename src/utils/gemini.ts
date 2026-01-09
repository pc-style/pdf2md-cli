import { GoogleGenerativeAI } from '@google/generative-ai';

export async function convertToMarkdown(text: string, apiKey: string, modelName: string = 'gemini-3-flash-preview'): Promise<string> {
  const genAI = new GoogleGenerativeAI(apiKey);
  const model = genAI.getGenerativeModel({ model: modelName });

  const prompt = `Convert the following raw PDF text into well-formatted markdown.
Rules:
- Use appropriate heading levels
- Format lists properly
- Preserve code blocks if present
- Add proper spacing
- Make it readable and well-structured
- Do not output any preamble or explanation, just the markdown.

Raw text:
${text}`;

  const result = await model.generateContent(prompt);
  const response = await result.response;
  return response.text();
}
