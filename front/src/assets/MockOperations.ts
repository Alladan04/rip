import defaultImage from './Default.svg';

const mockOperations = [
    {
        id: 1,
        img_src: "none",
        name: 'пример операции',
        description: 'лололололо',
        status: 'действует',
        image: defaultImage,
    }
]


export const getMockOperations = () => {
    return {
        operations: mockOperations,
    };
};