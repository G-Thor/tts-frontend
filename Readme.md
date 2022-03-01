# TTS Frontend Pipeline for Icelandic

This project provides a TTS frontend pipeline for Icelandic. The pipeline includes modules for html parsing, text cleaning, text normalization for TTS, spell and grammar correction, phrasing, and grapheme-to-phoneme (g2p) conversion. 

## The Pipeline

The TTS frontend pipeline makes seamless text preprocessing for TTS using different submodules possible. It manages tags, e.g. SSML tags, that might be added or processed at different stages, and stores the processing history of each token from original input, through normalizing and correction to phonetic representation at the end of the pipeline.