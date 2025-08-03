import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Loader2, Zap, Target, Settings } from 'lucide-react';
import { QuerySubmission, LLMProvider, LLM_PROVIDERS, SEO_CATEGORIES } from '@/types/llm';

interface QueryFormProps {
  onSubmit: (query: QuerySubmission) => void;
  isLoading?: boolean;
}

export const QueryForm: React.FC<QueryFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<QuerySubmission>({
    prompt: '',
    category: '',
    tags: [],
    providers: ['openai', 'claude'] // Default selection
  });

  const [tagInput, setTagInput] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Validation
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.prompt.trim()) {
      newErrors.prompt = 'SEO question is required';
    } else if (formData.prompt.length < 10) {
      newErrors.prompt = 'Please provide a more detailed question (at least 10 characters)';
    }

    if (formData.providers.length === 0) {
      newErrors.providers = 'Please select at least one LLM provider';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleProviderToggle = (provider: LLMProvider) => {
    setFormData(prev => ({
      ...prev,
      providers: prev.providers.includes(provider)
        ? prev.providers.filter(p => p !== provider)
        : [...prev.providers, provider]
    }));
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, tagInput.trim()]
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.currentTarget === document.activeElement) {
      e.preventDefault();
      handleAddTag();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="w-full max-w-4xl mx-auto shadow-elevated">
        <CardHeader className="text-center pb-6">
          <CardTitle className="text-3xl font-bold text-foreground flex items-center justify-center gap-3">
            <Zap className="h-8 w-8 text-primary" />
            LLM SEO Evaluator
          </CardTitle>
          <CardDescription className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Submit your SEO question to multiple AI models and get comparative analysis, 
            similarity scores, and quality insights.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* SEO Question Input */}
            <motion.div 
              className="space-y-3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
            >
              <Label htmlFor="prompt" className="text-base font-medium flex items-center gap-2">
                <Target className="h-4 w-4" />
                SEO Question or Prompt
              </Label>
              <Textarea
                id="prompt"
                placeholder="e.g., What are the best Python automation scripts for SEO in 2025? How can I improve my site's Core Web Vitals?"
                value={formData.prompt}
                onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
                className={`min-h-[120px] text-base ${errors.prompt ? 'border-destructive' : ''}`}
                disabled={isLoading}
              />
              {errors.prompt && (
                <p className="text-sm text-destructive">{errors.prompt}</p>
              )}
            </motion.div>

            {/* Category Selection */}
            <motion.div 
              className="space-y-3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              <Label className="text-base font-medium">Category (Optional)</Label>
              <Select 
                value={formData.category} 
                onValueChange={(value) => setFormData({ ...formData, category: value })}
                disabled={isLoading}
              >
                <SelectTrigger className="text-base">
                  <SelectValue placeholder="Select SEO category" />
                </SelectTrigger>
                <SelectContent>
                  {SEO_CATEGORIES.map((cat) => (
                    <SelectItem key={cat.value} value={cat.value}>
                      <div>
                        <div className="font-medium">{cat.label}</div>
                        <div className="text-sm text-muted-foreground">{cat.description}</div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </motion.div>

            {/* Tags Input */}
            <motion.div 
              className="space-y-3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <Label className="text-base font-medium">Tags (Optional)</Label>
              <div className="flex gap-2">
                <Input
                  placeholder="Add keywords (press Enter)"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1"
                  disabled={isLoading}
                />
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={handleAddTag}
                  disabled={!tagInput.trim() || isLoading}
                >
                  Add
                </Button>
              </div>
              {formData.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {formData.tags.map((tag) => (
                    <Badge 
                      key={tag} 
                      variant="secondary" 
                      className="cursor-pointer hover:bg-destructive hover:text-destructive-foreground transition-colors"
                      onClick={() => handleRemoveTag(tag)}
                    >
                      {tag} ×
                    </Badge>
                  ))}
                </div>
              )}
            </motion.div>

            {/* LLM Provider Selection */}
            <motion.div 
              className="space-y-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              <Label className="text-base font-medium flex items-center gap-2">
                <Settings className="h-4 w-4" />
                Select LLM Providers
              </Label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(LLM_PROVIDERS).map(([key, provider]) => (
                  <motion.div
                    key={key}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Card 
                      className={`cursor-pointer transition-all border-2 ${
                        formData.providers.includes(key as LLMProvider)
                          ? 'border-primary bg-primary/5 shadow-sm'
                          : 'border-border hover:border-primary/50'
                      }`}
                      onClick={() => handleProviderToggle(key as LLMProvider)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-3">
                          <Checkbox
                            id={key}
                            checked={formData.providers.includes(key as LLMProvider)}
                            onCheckedChange={() => handleProviderToggle(key as LLMProvider)}
                            disabled={isLoading}
                          />
                          <div className="flex-1">
                            <Label 
                              htmlFor={key} 
                              className="text-base font-medium cursor-pointer"
                            >
                              {provider.name}
                            </Label>
                            <p className="text-sm text-muted-foreground mt-1">
                              {provider.description}
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
              {errors.providers && (
                <p className="text-sm text-destructive">{errors.providers}</p>
              )}
            </motion.div>

            {/* Submit Button */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <Button
                type="submit"
                size="lg"
                className="w-full text-lg py-6 font-semibold"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Analyzing with {formData.providers.length} LLM{formData.providers.length > 1 ? 's' : ''}...
                  </>
                ) : (
                  <>
                    <Zap className="mr-2 h-5 w-5" />
                    Analyze with {formData.providers.length} LLM{formData.providers.length > 1 ? 's' : ''}
                  </>
                )}
              </Button>
            </motion.div>
          </form>

          {/* Quick Tips */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-8 p-4 bg-muted/50 rounded-lg"
          >
            <h4 className="font-medium text-sm mb-2">💡 Tips for better results:</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Be specific about your SEO goals and context</li>
              <li>• Include technical details when asking about implementation</li>
              <li>• Try multiple providers to see different perspectives</li>
              <li>• Use tags to organize and find your queries later</li>
            </ul>
          </motion.div>
        </CardContent>
      </Card>
    </motion.div>
  );
};