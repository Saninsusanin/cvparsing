import bs4.element


def paragraph_traverse(current_node, destination_file):
    """
    parse bs4 Node and save to file
    :param current_node: bs4 Node
    :param destination_file: path to output file
    :return: None
    """
    if isinstance(current_node, bs4.element.Tag):

        for node in current_node.contents:
            paragraph_traverse(node, destination_file)

        if 'class' in current_node.attrs:
            node_class = current_node['class']

            if node_class == 'ocrx_block':
                destination_file.write('\n')
            elif node_class == 'ocrx_word':
                destination_file.write(' ')

        if current_node.name == 'tr':
            destination_file.write('\n')
        if current_node == 'td':
            destination_file.write(' ')

    else:
        text = str.strip(str(current_node).replace('\u200b', '\n').replace('\xa0', '\n'))

        if len(text):
            destination_file.write(text)
