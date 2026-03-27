// import { useState, useRef, useEffect } from 'react';
// import { Upload, Send, Trash2, FileText, Bot } from 'lucide-react';
// import axios from 'axios';

// interface Message {
//   role: 'user' | 'assistant';
//   content: string;
//   sources?: any[];
// }

// const API_BASE = 'http://127.0.0.1:8000/api';

// function App() {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [input, setInput] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [documents, setDocuments] = useState<string[]>([]);
//   const [selectedDocument, setSelectedDocument] = useState<string | null>(null);

//   const chatEndRef = useRef<HTMLDivElement>(null);
//   const fileInputRef = useRef<HTMLInputElement>(null);

//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   const uploadFile = async (file: File) => {
//     const formData = new FormData();
//     formData.append('file', file);

//     try {
//       const res = await axios.post(`${API_BASE}/upload/`, formData, {
//         headers: { 'Content-Type': 'multipart/form-data' }
//       });

//       alert(`✅ Uploaded: ${file.name} (${res.data.chunks_stored} chunks)`);
//       setDocuments(prev => [...prev, file.name]);
//       setSelectedDocument(file.name);   // Auto-select the uploaded document
//     } catch (err: any) {
//       alert('Upload failed: ' + (err.response?.data?.detail || err.message));
//     }
//   };

//   const sendMessage = async () => {
//     if (!input.trim() || isLoading) return;

//     const userMessage: Message = { role: 'user', content: input };
//     setMessages(prev => [...prev, userMessage]);

//     const currentQuestion = input;
//     setInput('');
//     setIsLoading(true);

//     try {
//       // Pass the selected document as source if available
//       const url = selectedDocument 
//         ? `${API_BASE}/ask/?session_id=default&source=${encodeURIComponent(selectedDocument)}`
//         : `${API_BASE}/ask/?session_id=default`;

//       const response = await fetch(url, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ question: currentQuestion })
//       });

//       if (!response.ok) throw new Error('Failed to get response');

//       const reader = response.body?.getReader();
//       const decoder = new TextDecoder();
//       let assistantContent = '';
//       let sources: any[] = [];

//       const assistantMsg: Message = { role: 'assistant', content: '' };
//       setMessages(prev => [...prev, assistantMsg]);

//       if (reader) {
//         while (true) {
//           const { done, value } = await reader.read();
//           if (done) break;

//           const chunk = decoder.decode(value);
//           const lines = chunk.split('\n');

//           for (const line of lines) {
//             if (line.startsWith('data: ')) {
//               const data = line.slice(6).trim();

//               if (data.startsWith('[SOURCES]')) {
//                 try {
//                   sources = JSON.parse(data.slice(10));
//                 } catch (e) {}
//               } else if (data) {
//                 assistantContent += data;
//                 setMessages(prev => {
//                   const updated = [...prev];
//                   updated[updated.length - 1] = {
//                     role: 'assistant',
//                     content: assistantContent,
//                     sources: sources.length > 0 ? sources : undefined
//                   };
//                   return updated;
//                 });
//               }
//             }
//           }
//         }
//       }
//     } catch (err: any) {
//       console.error(err);
//       setMessages(prev => [...prev, {
//         role: 'assistant',
//         content: 'Sorry, something went wrong. Please try again.'
//       }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyPress = (e: React.KeyboardEvent) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       sendMessage();
//     }
//   };

//   return (
//     <div className="flex h-screen bg-zinc-950 text-white overflow-hidden">
//       {/* Sidebar */}
//       <div className="w-80 border-r border-zinc-800 bg-zinc-900 flex flex-col">
//         <div className="p-6 border-b border-zinc-800">
//           <div className="flex items-center gap-3">
//             <Bot className="w-8 h-8 text-blue-500" />
//             <div>
//               <h1 className="text-2xl font-bold">AI Knowledge Assistant</h1>
//               <p className="text-zinc-400 text-sm">Upload • Ask • Learn</p>
//             </div>
//           </div>
//         </div>

//         <div className="p-6">
//           <button
//             onClick={() => fileInputRef.current?.click()}
//             className="w-full bg-blue-600 hover:bg-blue-700 py-4 rounded-2xl flex items-center justify-center gap-3 font-medium transition-all"
//           >
//             <Upload className="w-5 h-5" />
//             Upload Document
//           </button>
//           <input
//             ref={fileInputRef}
//             type="file"
//             className="hidden"
//             accept=".pdf,.txt,.docx"
//             onChange={(e) => e.target.files && uploadFile(e.target.files[0])}
//           />
//         </div>

//         <div className="px-6 text-xs uppercase tracking-widest text-zinc-500 mb-3">UPLOADED DOCUMENTS</div>
//         <div className="flex-1 overflow-auto px-6 space-y-2">
//           {documents.length === 0 ? (
//             <p className="text-zinc-500 text-sm italic">No documents uploaded yet</p>
//           ) : (
//             documents.map((filename, i) => (
//               <div 
//                 key={i} 
//                 className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition cursor-pointer ${
//                   selectedDocument === filename ? 'bg-blue-600' : 'bg-zinc-800 hover:bg-zinc-700'
//                 }`}
//                 onClick={() => setSelectedDocument(filename)}
//               >
//                 <FileText className="w-4 h-4 text-blue-400" />
//                 <span className="truncate">{filename}</span>
//               </div>
//             ))
//           )}
//         </div>
//       </div>

//       {/* Chat Area */}
//       <div className="flex-1 flex flex-col">
//         <div className="p-6 border-b border-zinc-800 flex items-center justify-between">
//           <h2 className="text-xl font-semibold">Chat with your Documents</h2>
//           {selectedDocument && (
//             <div className="text-sm text-blue-400">Searching in: {selectedDocument}</div>
//           )}
//         </div>

//         <div className="flex-1 overflow-auto p-8 space-y-8">
//           {messages.length === 0 && (
//             <div className="text-center mt-32 text-zinc-500">
//               Select or upload a document and start asking questions
//             </div>
//           )}

//           {messages.map((msg, index) => (
//             <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
//               <div className={`max-w-3xl rounded-3xl px-6 py-4 ${msg.role === 'user' 
//                 ? 'bg-blue-600' 
//                 : 'bg-zinc-800'}`}>
//                 <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                
//                 {msg.sources && msg.sources.length > 0 && (
//                   <div className="mt-4 pt-4 border-t border-zinc-700 text-xs text-blue-400">
//                     Sources: {msg.sources.map(s => s.source).join(', ')}
//                   </div>
//                 )}
//               </div>
//             </div>
//           ))}

//           {isLoading && (
//             <div className="flex justify-start">
//               <div className="bg-zinc-800 rounded-3xl px-6 py-4">
//                 <div className="flex gap-1">
//                   <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" />
//                   <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce delay-150" />
//                   <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce delay-300" />
//                 </div>
//               </div>
//             </div>
//           )}

//           <div ref={chatEndRef} />
//         </div>

//         {/* Input Area */}
//         <div className="p-6 border-t border-zinc-800 bg-zinc-900">
//           <div className="max-w-4xl mx-auto flex gap-3">
//             <input
//               type="text"
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               onKeyPress={handleKeyPress}
//               placeholder="Ask anything about your documents..."
//               className="flex-1 bg-zinc-800 border border-zinc-700 rounded-2xl px-6 py-4 focus:outline-none focus:border-blue-500"
//               disabled={isLoading}
//             />
//             <button
//               onClick={sendMessage}
//               disabled={!input.trim() || isLoading}
//               className="bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-700 px-8 rounded-2xl flex items-center justify-center"
//             >
//               <Send className="w-6 h-6" />
//             </button>
//           </div>
//           <p className="text-center text-xs text-zinc-500 mt-3">
//             Streaming enabled • Powered by Groq + ChromaDB
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

import { useState, useRef, useEffect } from 'react';
import { Upload, Send, FileText, Bot } from 'lucide-react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
}

const API_BASE = 'http://127.0.0.1:8000/api';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [documents, setDocuments] = useState<string[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // General cleaning - works for ANY PDF, no hardcoded names
  const cleanText = (text: string): string => {
    let cleaned = text
      // Fix single letter + space + letter (most common break)
      .replace(/(\b\w)\s+(\w\b)/g, '$1$2')
      // Fix two-letter + space + two-letter
      .replace(/(\b\w\w)\s+(\w\w\b)/g, '$1$2')
      // Fix letter + space + two letters
      .replace(/(\b\w)\s+(\w\w\b)/g, '$1$2')
      // Fix repeated letters (e.g., "ee eee" → "eee")
      .replace(/(\w)\s+\1+/g, '$1')
      // Fix glued punctuation
      .replace(/\s+([.,:;!?])/g, '$1')
      .replace(/([.,:;!?])\s+/g, '$1 ')
      // Normalize multiple spaces
      .replace(/\s+/g, ' ')
      // Basic sentence capitalization
      .replace(/([.!?]\s+)([a-z])/g, (m, p1, p2) => p1 + p2.toUpperCase());

    return cleaned.trim();
  };

  const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_BASE}/upload/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      alert(`✅ Uploaded: ${file.name} (${res.data.chunks_stored || 0} chunks)`);
      setDocuments(prev => [...prev, file.name]);
      setSelectedDocument(file.name);
    } catch (err: any) {
      alert('Upload failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);

    const currentQuestion = input;
    setInput('');
    setIsLoading(true);

    try {
      const url = selectedDocument 
        ? `${API_BASE}/ask/?session_id=default&source=${encodeURIComponent(selectedDocument)}`
        : `${API_BASE}/ask/?session_id=default`;

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: currentQuestion })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantContent = '';
      let sources: any[] = [];

      const assistantMsg: Message = { role: 'assistant', content: '' };
      setMessages(prev => [...prev, assistantMsg]);

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              let data = line.slice(6).trim();

              if (data.startsWith('[SOURCES]')) {
                try {
                  sources = JSON.parse(data.slice(10));
                } catch (e) {}
              } else if (data) {
                if (assistantContent && !assistantContent.endsWith(' ') && !data.startsWith(' ')) {
                  assistantContent += ' ';
                }
                assistantContent += data;

                const cleaned = cleanText(assistantContent);

                setMessages(prev => {
                  const updated = [...prev];
                  updated[updated.length - 1] = {
                    role: 'assistant',
                    content: cleaned,
                    sources: sources.length > 0 ? sources : undefined
                  };
                  return updated;
                });
              }
            }
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-zinc-950 text-white overflow-hidden">
      {/* Sidebar */}
      <div className="w-80 border-r border-zinc-800 bg-zinc-900 flex flex-col">
        <div className="p-6 border-b border-zinc-800">
          <div className="flex items-center gap-3">
            <Bot className="w-8 h-8 text-blue-500" />
            <div>
              <h1 className="text-2xl font-bold">AI Knowledge Assistant</h1>
              <p className="text-zinc-400 text-sm">Upload • Ask • Learn</p>
            </div>
          </div>
        </div>

        <div className="p-6">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full bg-blue-600 hover:bg-blue-700 py-4 rounded-2xl flex items-center justify-center gap-3 font-medium transition-all active:scale-95"
          >
            <Upload className="w-5 h-5" />
            Upload Document
          </button>
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept=".pdf,.txt,.docx"
            onChange={(e) => e.target.files && uploadFile(e.target.files[0])}
          />
        </div>

        <div className="px-6 text-xs uppercase tracking-widest text-zinc-500 mb-3">UPLOADED DOCUMENTS</div>
        <div className="flex-1 overflow-auto px-6 space-y-2">
          {documents.length === 0 ? (
            <p className="text-zinc-500 text-sm italic px-2">No documents uploaded yet</p>
          ) : (
            documents.map((filename, i) => (
              <div 
                key={i} 
                className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition cursor-pointer ${
                  selectedDocument === filename ? 'bg-blue-600 text-white' : 'bg-zinc-800 hover:bg-zinc-700'
                }`}
                onClick={() => setSelectedDocument(filename)}
              >
                <FileText className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{filename}</span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="p-6 border-b border-zinc-800 flex items-center justify-between bg-zinc-900">
          <h2 className="text-xl font-semibold">Chat with your Documents</h2>
          {selectedDocument && (
            <div className="text-sm text-blue-400">Searching in: {selectedDocument}</div>
          )}
        </div>

        <div className="flex-1 overflow-auto p-8 space-y-8 bg-zinc-950">
          {messages.length === 0 && (
            <div className="text-center mt-32 text-zinc-500">
              Upload a document from the sidebar and start asking questions
            </div>
          )}

          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl rounded-3xl px-6 py-4 ${msg.role === 'user' ? 'bg-blue-600' : 'bg-zinc-800'}`}>
                <p className="whitespace-pre-wrap leading-relaxed break-words">{msg.content}</p>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-zinc-700 text-xs text-blue-400">
                    Sources: {msg.sources.map(s => s.source).join(', ')}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-zinc-800 rounded-3xl px-6 py-4">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce delay-150" />
                  <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce delay-300" />
                </div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 border-t border-zinc-800 bg-zinc-900">
          <div className="max-w-4xl mx-auto flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask anything about your documents..."
              className="flex-1 bg-zinc-800 border border-zinc-700 rounded-2xl px-6 py-4 focus:outline-none focus:border-blue-500 disabled:opacity-50"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-700 px-8 rounded-2xl flex items-center justify-center transition-all"
            >
              <Send className="w-6 h-6" />
            </button>
          </div>
          <p className="text-center text-xs text-zinc-500 mt-3">
            Streaming enabled • Powered by Groq + ChromaDB
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;