/*************************************************************************/
/*  platform_config.h                                                    */
/*************************************************************************/
/*                       This file is part of:                           */
/*                           GODOT ENGINE                                */
/*                    http://www.godotengine.org                         */
/*************************************************************************/
/* Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.                 */
/*                                                                       */
/* Permission is hereby granted, free of charge, to any person obtaining */
/* a copy of this software and associated documentation files (the       */
/* "Software"), to deal in the Software without restriction, including   */
/* without limitation the rights to use, copy, modify, merge, publish,   */
/* distribute, sublicense, and/or sell copies of the Software, and to    */
/* permit persons to whom the Software is furnished to do so, subject to */
/* the following conditions:                                             */
/*                                                                       */
/* The above copyright notice and this permission notice shall be        */
/* included in all copies or substantial portions of the Software.       */
/*                                                                       */
/* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       */
/* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    */
/* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.*/
/* IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY  */
/* CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,  */
/* TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE     */
/* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                */
/*************************************************************************/
#define Mutex Lib3dsMutex
#define Semaphore Lib3dsSemaphore
#define Thread Lib3dsThread
#define AudioDriver Lib3dsAudioDriver
#define KEY_UP KEY3DS_UP
#define KEY_DOWN KEY3DS_DOWN
#define KEY_LEFT KEY3DS_LEFT
#define KEY_RIGHT KEY3DS_RIGHT
#define KEY_L KEY3DS_L
#define KEY_R KEY3DS_R
#define KEY_A KEY3DS_A
#define KEY_B KEY3DS_B
#define KEY_X KEY3DS_X
#define KEY_Y KEY3DS_Y

#include <3ds.h>
#undef AudioDriver
#undef Thread
#undef Mutex
#undef Semaphore
#undef KEY_UP
#undef KEY_DOWN
#undef KEY_LEFT
#undef KEY_RIGHT
#undef KEY_L
#undef KEY_R
#undef KEY_A
#undef KEY_B
#undef KEY_X
#undef KEY_Y
