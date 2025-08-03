import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { QueryResults } from '@/types/llm';
import { format } from 'date-fns';

interface PDFExportOptions {
  includeMetrics?: boolean;
  includeResponses?: boolean;
  includeComparison?: boolean;
  format?: 'detailed' | 'summary';
}

export class PDFExportService {
  private doc: jsPDF;
  private currentY: number = 20;
  private readonly pageWidth: number = 210; // A4 width in mm
  private readonly pageHeight: number = 297; // A4 height in mm
  private readonly margin: number = 20;
  private readonly lineHeight: number = 7;

  constructor() {
    this.doc = new jsPDF();
  }

  async exportResults(
    results: QueryResults, 
    options: PDFExportOptions = {
      includeMetrics: true,
      includeResponses: true,
      includeComparison: true,
      format: 'detailed'
    }
  ): Promise<void> {
    try {
      // Initialize PDF
      this.setupDocument();
      
      // Add header and title
      this.addHeader(results);
      
      // Add query information
      this.addQueryInfo(results.query);
      
      // Add executive summary
      this.addExecutiveSummary(results);
      
      if (options.includeMetrics) {
        this.addMetricsOverview(results.evaluation_metrics);
      }
      
      if (options.includeComparison) {
        this.addComparisonMatrix(results.evaluation_metrics);
      }
      
      if (options.includeResponses) {
        this.addResponseDetails(results.responses, options.format);
      }
      
      // Add footer
      this.addFooter();
      
      // Generate filename and download
      const filename = this.generateFilename(results.query.prompt);
      this.doc.save(filename);
      
    } catch (error) {
      console.error('PDF export failed:', error);
      throw new Error('Failed to generate PDF report');
    }
  }

  private setupDocument(): void {
    this.doc.setProperties({
      title: 'LLM SEO Evaluation Report',
      subject: 'AI Response Analysis Report',
      author: 'LLM SEO Evaluator',
      creator: 'LLM SEO Evaluator v1.0'
    });
  }

  private addHeader(results: QueryResults): void {
    // Title
    this.doc.setFontSize(24);
    this.doc.setFont('helvetica', 'bold');
    this.doc.text('LLM SEO Evaluation Report', this.margin, this.currentY);
    
    this.currentY += 15;
    
    // Subtitle with query preview
    this.doc.setFontSize(14);
    this.doc.setFont('helvetica', 'normal');
    const queryPreview = results.query.prompt.length > 60 
      ? results.query.prompt.substring(0, 60) + '...'
      : results.query.prompt;
    this.doc.text(`Analysis of: "${queryPreview}"`, this.margin, this.currentY);
    
    this.currentY += 10;
    
    // Date and providers
    this.doc.setFontSize(10);
    this.doc.setTextColor(100);
    this.doc.text(`Generated: ${format(new Date(), 'PPP')}`, this.margin, this.currentY);
    this.doc.text(`Providers: ${results.query.providers.length}`, this.pageWidth - this.margin - 30, this.currentY);
    
    this.currentY += 15;
    this.addSeparator();
  }

  private addQueryInfo(query: any): void {
    this.addSectionTitle('Query Information');
    
    this.doc.setFontSize(10);
    this.doc.setTextColor(0);
    
    // Query details
    this.addField('Prompt:', query.prompt, true);
    this.addField('Category:', query.category);
    this.addField('Tags:', query.tags.join(', '));
    this.addField('Providers:', query.providers.join(', '));
    this.addField('Submitted:', format(new Date(query.created_at), 'PPp'));
    
    this.currentY += 10;
  }

  private addExecutiveSummary(results: QueryResults): void {
    this.addSectionTitle('Executive Summary');
    
    const metrics = results.evaluation_metrics.response_metrics;
    const avgOriginality = Object.values(metrics).reduce((sum, m) => sum + m.originality_score, 0) / Object.values(metrics).length;
    const avgReadability = Object.values(metrics).reduce((sum, m) => sum + m.readability_score, 0) / Object.values(metrics).length;
    
    this.doc.setFontSize(10);
    this.doc.setTextColor(0);
    
    const summary = [
      `• Evaluated ${results.responses.length} responses from different LLM providers`,
      `• Average originality score: ${avgOriginality.toFixed(1)}/10`,
      `• Average readability score: ${avgReadability.toFixed(1)}/10`,
      `• Response similarity ranges from ${Math.min(...results.evaluation_metrics.similarity_matrix.flat().filter(v => v !== 1.0)).toFixed(2)} to ${Math.max(...results.evaluation_metrics.similarity_matrix.flat().filter(v => v !== 1.0)).toFixed(2)}`,
      `• Total unique tools mentioned: ${new Set(Object.values(metrics).flatMap(m => m.tool_mentions)).size}`
    ];
    
    summary.forEach(line => {
      this.doc.text(line, this.margin, this.currentY);
      this.currentY += this.lineHeight;
    });
    
    this.currentY += 10;
  }

  private addMetricsOverview(metrics: any): void {
    this.addSectionTitle('Performance Metrics');
    
    this.doc.setFontSize(9);
    this.doc.setFont('helvetica', 'bold');
    
    // Table headers
    const headers = ['Provider', 'Originality', 'Readability', 'Keywords', 'Tools'];
    const colWidths = [40, 25, 25, 25, 45];
    let currentX = this.margin;
    
    headers.forEach((header, i) => {
      this.doc.text(header, currentX, this.currentY);
      currentX += colWidths[i];
    });
    
    this.currentY += this.lineHeight;
    this.addLine();
    
    // Table data
    this.doc.setFont('helvetica', 'normal');
    Object.entries(metrics.response_metrics).forEach(([provider, data]: [string, any]) => {
      currentX = this.margin;
      const rowData = [
        provider.toUpperCase(),
        data.originality_score.toFixed(1),
        data.readability_score.toFixed(1),
        data.keyword_count.toString(),
        data.tool_mentions.length.toString()
      ];
      
      rowData.forEach((value, i) => {
        this.doc.text(value, currentX, this.currentY);
        currentX += colWidths[i];
      });
      
      this.currentY += this.lineHeight;
    });
    
    this.currentY += 10;
  }

  private addComparisonMatrix(metrics: any): void {
    this.addSectionTitle('Provider Similarity Matrix');
    
    this.doc.setFontSize(8);
    this.doc.text('Values represent similarity scores between providers (0.0 = completely different, 1.0 = identical)', 
      this.margin, this.currentY);
    this.currentY += 10;
    
    const providers = Object.keys(metrics.response_metrics);
    const matrix = metrics.similarity_matrix;
    
    // Matrix headers
    this.doc.setFont('helvetica', 'bold');
    let currentX = this.margin + 30;
    providers.forEach(provider => {
      this.doc.text(provider.substring(0, 6).toUpperCase(), currentX, this.currentY);
      currentX += 25;
    });
    
    this.currentY += this.lineHeight;
    
    // Matrix data
    this.doc.setFont('helvetica', 'normal');
    providers.forEach((provider, i) => {
      currentX = this.margin;
      this.doc.text(provider.toUpperCase(), currentX, this.currentY);
      currentX += 30;
      
      matrix[i].forEach((value: number) => {
        const color = value === 1.0 ? 0 : value > 0.7 ? 150 : value > 0.5 ? 100 : 50;
        this.doc.setTextColor(color);
        this.doc.text(value.toFixed(2), currentX, this.currentY);
        currentX += 25;
      });
      
      this.doc.setTextColor(0);
      this.currentY += this.lineHeight;
    });
    
    this.currentY += 10;
  }

  private addResponseDetails(responses: any[], format?: string): void {
    responses.forEach((response, index) => {
      // Check if we need a new page
      if (this.currentY > this.pageHeight - 60) {
        this.doc.addPage();
        this.currentY = 20;
      }
      
      this.addSectionTitle(`${response.provider.toUpperCase()} Response (${response.model})`);
      
      // Response metadata
      this.doc.setFontSize(9);
      this.doc.setTextColor(100);
      this.doc.text(`Tokens: ${response.metadata.tokens_used} | Response Time: ${response.metadata.response_time_ms}ms`, 
        this.margin, this.currentY);
      this.currentY += 10;
      
      // Response content (truncated for PDF)
      this.doc.setFontSize(9);
      this.doc.setTextColor(0);
      
      const maxLength = format === 'summary' ? 300 : 800;
      const content = response.response_text.length > maxLength 
        ? response.response_text.substring(0, maxLength) + '...\n\n[Content truncated for PDF report]'
        : response.response_text;
      
      // Split text into lines that fit the page width
      const lines = this.doc.splitTextToSize(content, this.pageWidth - 2 * this.margin);
      
      lines.forEach((line: string) => {
        if (this.currentY > this.pageHeight - 30) {
          this.doc.addPage();
          this.currentY = 20;
        }
        this.doc.text(line, this.margin, this.currentY);
        this.currentY += this.lineHeight;
      });
      
      this.currentY += 15;
    });
  }

  private addSectionTitle(title: string): void {
    this.doc.setFontSize(14);
    this.doc.setFont('helvetica', 'bold');
    this.doc.setTextColor(0);
    this.doc.text(title, this.margin, this.currentY);
    this.currentY += 10;
  }

  private addField(label: string, value: string, multiline = false): void {
    this.doc.setFont('helvetica', 'bold');
    this.doc.text(label, this.margin, this.currentY);
    
    this.doc.setFont('helvetica', 'normal');
    if (multiline && value.length > 80) {
      const lines = this.doc.splitTextToSize(value, this.pageWidth - 2 * this.margin - 30);
      this.doc.text(lines[0], this.margin + 30, this.currentY);
      
      for (let i = 1; i < lines.length; i++) {
        this.currentY += this.lineHeight;
        this.doc.text(lines[i], this.margin + 30, this.currentY);
      }
    } else {
      this.doc.text(value, this.margin + 30, this.currentY);
    }
    
    this.currentY += this.lineHeight + 2;
  }

  private addSeparator(): void {
    this.doc.setDrawColor(200);
    this.doc.line(this.margin, this.currentY, this.pageWidth - this.margin, this.currentY);
    this.currentY += 10;
  }

  private addLine(): void {
    this.doc.setDrawColor(150);
    this.doc.line(this.margin, this.currentY, this.pageWidth - this.margin, this.currentY);
    this.currentY += 5;
  }

  private addFooter(): void {
    const pageCount = this.doc.getNumberOfPages();
    
    for (let i = 1; i <= pageCount; i++) {
      this.doc.setPage(i);
      this.doc.setFontSize(8);
      this.doc.setTextColor(150);
      
      // Page number
      this.doc.text(`Page ${i} of ${pageCount}`, this.pageWidth - this.margin - 20, this.pageHeight - 10);
      
      // Footer text
      this.doc.text('Generated by LLM SEO Evaluator', this.margin, this.pageHeight - 10);
    }
  }

  private generateFilename(prompt: string): string {
    const timestamp = format(new Date(), 'yyyy-MM-dd_HHmm');
    const cleanPrompt = prompt
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(' ')
      .slice(0, 4)
      .join('-');
    
    return `llm-analysis_${cleanPrompt}_${timestamp}.pdf`;
  }
}

// Export singleton instance
export const pdfExportService = new PDFExportService();