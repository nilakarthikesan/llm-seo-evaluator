import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Download, FileText, Loader2, CheckCircle } from 'lucide-react';
import { QueryResults } from '@/types/llm';
// import { pdfExportService } from '@/services/pdfExport';
import { useToast } from '@/hooks/use-toast';

interface ExportPDFProps {
  results: QueryResults;
  className?: string;
}

interface ExportOptions {
  includeMetrics: boolean;
  includeResponses: boolean;
  includeComparison: boolean;
  format: 'detailed' | 'summary';
}

export const ExportPDF: React.FC<ExportPDFProps> = ({ results, className = '' }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [options, setOptions] = useState<ExportOptions>({
    includeMetrics: true,
    includeResponses: true,
    includeComparison: true,
    format: 'detailed'
  });
  const { toast } = useToast();

  const handleExport = async () => {
    setIsExporting(true);
    setIsSuccess(false);
    
    try {
      // Temporarily disabled PDF export functionality
      // await pdfExportService.exportResults(results, options);
      
      // Simulate export for now
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setIsSuccess(true);
      toast({
        title: "PDF Export (Demo) 📄",
        description: "PDF export functionality will be available soon. This is a demo of the interface.",
      });
      
      // Reset success state after 3 seconds
      setTimeout(() => setIsSuccess(false), 3000);
      
    } catch (error) {
      console.error('PDF export failed:', error);
      toast({
        title: "Export Failed",
        description: "There was an error generating the PDF report. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsExporting(false);
    }
  };

  const updateOption = (key: keyof ExportOptions, value: any) => {
    setOptions(prev => ({ ...prev, [key]: value }));
  };

  const getEstimatedPages = (): number => {
    let pages = 2; // Base pages for header, summary, metrics
    
    if (options.includeComparison) pages += 1;
    if (options.includeResponses) {
      pages += options.format === 'detailed' 
        ? Math.ceil(results.responses.length * 1.5)
        : Math.ceil(results.responses.length * 0.8);
    }
    
    return pages;
  };

  return (
    <div className={`space-y-6 ${className}`}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Export PDF Report
          </CardTitle>
          <CardDescription>
            Generate a comprehensive PDF report of your LLM analysis results
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Export Options */}
          <div className="space-y-4">
            <h4 className="text-sm font-medium">Report Configuration</h4>
            
            {/* Format Selection */}
            <div className="space-y-2">
              <Label htmlFor="format-select">Report Format</Label>
              <Select 
                value={options.format} 
                onValueChange={(value: 'detailed' | 'summary') => updateOption('format', value)}
              >
                <SelectTrigger id="format-select">
                  <SelectValue placeholder="Select format" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="detailed">Detailed Report (Full Content)</SelectItem>
                  <SelectItem value="summary">Summary Report (Key Points)</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                {options.format === 'detailed' 
                  ? 'Includes complete response content and analysis'
                  : 'Condensed version with key insights and metrics only'
                }
              </p>
            </div>

            {/* Content Options */}
            <div className="space-y-4">
              <h5 className="text-sm font-medium">Include Sections</h5>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="include-metrics">Performance Metrics</Label>
                    <p className="text-xs text-muted-foreground">
                      Originality scores, readability, keyword counts
                    </p>
                  </div>
                  <Switch
                    id="include-metrics"
                    checked={options.includeMetrics}
                    onCheckedChange={(checked) => updateOption('includeMetrics', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="include-comparison">Comparison Matrix</Label>
                    <p className="text-xs text-muted-foreground">
                      Provider similarity analysis and cross-comparisons
                    </p>
                  </div>
                  <Switch
                    id="include-comparison"
                    checked={options.includeComparison}
                    onCheckedChange={(checked) => updateOption('includeComparison', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="include-responses">Full Responses</Label>
                    <p className="text-xs text-muted-foreground">
                      Complete text responses from each provider
                    </p>
                  </div>
                  <Switch
                    id="include-responses"
                    checked={options.includeResponses}
                    onCheckedChange={(checked) => updateOption('includeResponses', checked)}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Export Info */}
          <div className="p-4 bg-muted/30 rounded-lg">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Estimated pages:</span>
              <span className="font-medium">{getEstimatedPages()} pages</span>
            </div>
            <div className="flex items-center justify-between text-sm mt-1">
              <span className="text-muted-foreground">File format:</span>
              <span className="font-medium">PDF</span>
            </div>
            <div className="flex items-center justify-between text-sm mt-1">
              <span className="text-muted-foreground">Query:</span>
              <span className="font-medium text-right max-w-[200px] truncate">
                {results.query.prompt}
              </span>
            </div>
          </div>

          {/* Export Button */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              onClick={handleExport}
              disabled={isExporting}
              className="w-full"
              size="lg"
            >
              {isExporting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating PDF...
                </>
              ) : isSuccess ? (
                <>
                  <CheckCircle className="mr-2 h-4 w-4" />
                  Downloaded Successfully!
                </>
              ) : (
                <>
                  <Download className="mr-2 h-4 w-4" />
                  Download PDF Report
                </>
              )}
            </Button>
          </motion.div>

          {/* Help Text */}
          <p className="text-xs text-muted-foreground text-center">
            The PDF will be saved to your default downloads folder
          </p>
        </CardContent>
      </Card>
    </div>
  );
};