import { GoogleGenerativeAI } from "@google/generative-ai";
import { NextResponse } from "next/server";

const apiKey = process.env.GEMINI_API_KEY;

export async function POST(req: Request) {
    if (!apiKey) {
        return NextResponse.json({ error: "Gemini API Key not configured" }, { status: 500 });
    }

    try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

        const { habitName, habitDesc } = await req.json();

        // Updated prompt to be more explicit about array structure and "3 pros, 3 cons"
        const prompt = `
      Analyze the habit "${habitName}" (${habitDesc}).
      Provide:
      1. A short, punchy feedback summary (max 5 words).
      2. Exactly 3 distinct advantages (pros).
      3. Exactly 3 distinct disadvantages (cons).
      
      CRITICAL: Return ONLY valid JSON with no markdown formatting. Structure:
      {
        "feedback": "string",
        "pros": ["string", "string", "string"],
        "cons": ["string", "string", "string"]
      }
    `;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        // Enhanced cleanup to handle potential markdown code blocks or whitespace
        const cleanText = text.replace(/```json/g, "").replace(/```/g, "").trim();

        let analysisData;
        try {
            analysisData = JSON.parse(cleanText);
        } catch (parseError) {
            console.error("JSON Parse Error:", parseError, "Raw Text:", text);
            return NextResponse.json({
                error: "Failed to parse AI response",
                details: "The AI returned an invalid format."
            }, { status: 500 });
        }

        // Validate structure
        if (!Array.isArray(analysisData.pros) || !Array.isArray(analysisData.cons)) {
            return NextResponse.json({
                error: "Invalid data structure",
                details: "AI did not return lists for pros/cons."
            }, { status: 500 });
        }

        return NextResponse.json(analysisData);

    } catch (error: any) {
        console.error("Gemini Error:", error);
        // Return the actual error message for debugging
        return NextResponse.json({
            error: "Failed to analyze habit",
            details: error.message || String(error)
        }, { status: 500 });
    }
}
