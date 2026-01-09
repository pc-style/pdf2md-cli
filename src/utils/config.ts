import Conf from 'conf';

const schema = {
	apiKey: {
		type: 'string',
        default: ''
	}
};

const config = new Conf({
    projectName: 'pdf2md-cli',
    schema
});

export function getApiKey(): string {
    return config.get('apiKey') as string;
}

export function setApiKey(key: string): void {
    config.set('apiKey', key);
}

export function deleteApiKey(): void {
    config.delete('apiKey');
}
