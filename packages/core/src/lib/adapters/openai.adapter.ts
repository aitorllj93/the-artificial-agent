import { OpenAIApi, Configuration, CreateCompletionRequest } from 'openai';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class OpenAIAdapter {
  private readonly logger = new Logger(OpenAIAdapter.name);

  private readonly configuration = new Configuration({
    apiKey: this.config.get('providers.openai.apiKey'),
  });

  private readonly openai = new OpenAIApi(this.configuration);

  private readonly defaultParams: Partial<CreateCompletionRequest> =
    this.config.get('providers.openai.completionParams') || {
      model: 'text-davinci-003',
      temperature: 0.7,
      max_tokens: 256,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
    };

  constructor(private config: ConfigService) {}

  public async generateTextFromPrompt(
    prompt: string,
    params?: Partial<CreateCompletionRequest>
  ): Promise<string> {
    const response = await this.openai.createCompletion({
      prompt,
      ...this.defaultParams,
      ...params,
    } as CreateCompletionRequest);

    this.logger.log(`Generated text: ${response.data.choices[0].text}`);

    return response.data.choices[0].text;
  }
}
