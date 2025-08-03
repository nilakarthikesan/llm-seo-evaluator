import React, { useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { QueryForm } from '@/components/query/QueryForm';
import { QuerySubmission } from '@/types/llm';
import { apiClient } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const handleQuerySubmit = async (queryData: QuerySubmission) => {
    setIsSubmitting(true);
    
    try {
      console.log('Submitting query:', queryData);
      const response = await apiClient.submitQuery(queryData);
      
      toast({
        title: "Query Submitted Successfully! 🚀",
        description: `Query ${response.query_id} is being processed by ${queryData.providers.length} LLM providers.`,
      });
      
      // TODO: Navigate to progress/results page
      console.log('Query response:', response);
      
    } catch (error) {
      console.error('Error submitting query:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your query. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout>
      <div className="space-y-8">
        <QueryForm 
          onSubmit={handleQuerySubmit}
          isLoading={isSubmitting}
        />
      </div>
    </Layout>
  );
};

export default Index;
