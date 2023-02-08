import { readFile, writeFile } from 'node:fs/promises';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkFrontmatter from 'remark-frontmatter';
import remarkStringify from 'remark-stringify';
import { Root } from 'remark-parse/lib';

const markdownProcessor = unified()
  .use(remarkParse)
  .use(remarkFrontmatter, ['yaml', 'toml']);

export const getHeadedSection = (sectionName: string, ast: Root) => {
  const sectionHeading = ast.children.find(
    (node) =>
      node.type === 'heading' && (node.children[0] as any).value === sectionName
  );

  if (!sectionHeading) {
    throw new Error('Section does not exist');
  }

  const sectionHeadingIndex = ast.children.indexOf(sectionHeading as any);

  const nextSectionHeadingIndex = ast.children.findIndex(
    (node, index) =>
      node.type === 'heading' &&
      node.depth <= (sectionHeading as any).depth &&
      index > sectionHeadingIndex
  );

  const sectionContent = ast.children.slice(
    sectionHeadingIndex + 1,
    nextSectionHeadingIndex === -1 ? undefined : nextSectionHeadingIndex
  );

  return {
    sectionHeading,
    sectionContent,
  };
};

export const getNoteAST = async (notePath: string): Promise<Root> => {
  const noteContent = await readFile(notePath, 'utf-8');

  const ast = await markdownProcessor.parse(noteContent);

  return ast;
};

export const getNoteSection = async (notePath: string, sectionName: string) => {
  const ast = await getNoteAST(notePath);

  const sectionContent = getHeadedSection(sectionName, ast);

  return sectionContent;
};

export const insertIntoSection = async (
  notePath: string,
  sectionName: string,
  content: string
) => {
  const { sectionContent, sectionHeading } = await getNoteSection(
    notePath,
    sectionName
  );

  const lastNode = sectionContent.length
    ? sectionContent[sectionContent.length - 1]
    : sectionHeading;

  const lastLine = lastNode.position.end.line;

  const noteContent = await readFile(notePath, 'utf-8');

  const noteContentArray = noteContent.split('\n');

  noteContentArray.splice(lastLine, 0, content);

  await writeFile(notePath, noteContentArray.join('\n'));
};

export const replaceLine = async (
  notePath: string,
  line: number,
  content: string
) => {
  const noteContent = await readFile(notePath, 'utf-8');

  const noteContentArray = noteContent.split('\n');

  noteContentArray.splice(line - 1, 1, content);

  await writeFile(notePath, noteContentArray.join('\n'));
};
