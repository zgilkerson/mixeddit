import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { MixedditError } from './mixeddit-error';
import { ErrorObservable } from 'rxjs/observable/ErrorObservable';

@Injectable()
export class MixedditErrorService {

  constructor() { }

  handleError(error: HttpErrorResponse) {
    const errorJson = JSON.parse(JSON.stringify(error.error));
    const mixedditError: MixedditError = {
      status: errorJson['error']['status'],
      message: errorJson['error']['message']
    };
    return new ErrorObservable(mixedditError);
  }
}
